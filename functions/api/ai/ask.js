import {
  PUBLIC_AI_GROUNDING,
  PUBLIC_AI_GROUNDING_SHA256,
} from "./_grounding.js";


const ALLOWED_LANGUAGES = new Set(["ru", "en"]);
const EXPECTED_FIELDS = ["language", "question", "session"];
const MAX_BODY_BYTES = 4096;
const MAX_QUESTION_CHARACTERS = 600;
const SESSION_PATTERN = /^[A-Za-z0-9_-]{16,96}$/;
const URL_PATTERN = /(?:https?:\/\/|www\.)/i;
const CONTROL_PATTERN = /[\u0000-\u001f\u007f]/;
const HASH_PATTERN = /^[a-f0-9]{64}$/;

const BASE_HEADERS = Object.freeze({
  "Cache-Control": "no-store",
  "Content-Type": "application/json; charset=utf-8",
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
});

const DISABLED_MESSAGE = Object.freeze({
  ru: "AI-ассистент проходит серверную подготовку. Пока используйте локальный режим публичных фактов на странице.",
  en: "The AI assistant is undergoing server-side preparation. For now, use the page's local public-facts mode.",
});


function jsonResponse(status, body, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {...BASE_HEADERS, ...headers},
  });
}


function errorResponse(status, code, message, headers = {}) {
  return jsonResponse(status, {error: {code, message}}, headers);
}


function hasExactFields(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  const keys = Object.keys(value).sort();
  return keys.length === EXPECTED_FIELDS.length
    && keys.every((key, index) => key === EXPECTED_FIELDS[index]);
}


function groundingIsReady() {
  return HASH_PATTERN.test(PUBLIC_AI_GROUNDING_SHA256)
    && PUBLIC_AI_GROUNDING?.contract_id === "public-ai-assistant-v0"
    && PUBLIC_AI_GROUNDING?.claims?.length === 25
    && PUBLIC_AI_GROUNDING?.relations?.length === 39
    && PUBLIC_AI_GROUNDING?.sources?.length > 0;
}


export async function handleRequest(request) {
  if (!(request instanceof Request)) {
    return errorResponse(500, "invalid_runtime_request", "Invalid runtime request.");
  }
  if (request.method !== "POST") {
    return errorResponse(
      405,
      "method_not_allowed",
      "Only POST is allowed.",
      {Allow: "POST"},
    );
  }

  const requestUrl = new URL(request.url);
  const origin = request.headers.get("Origin");
  if (origin !== requestUrl.origin) {
    return errorResponse(403, "same_origin_required", "A same-origin request is required.");
  }

  const contentType = (request.headers.get("Content-Type") || "")
    .split(";", 1)[0]
    .trim()
    .toLowerCase();
  if (contentType !== "application/json") {
    return errorResponse(415, "json_required", "Content-Type must be application/json.");
  }

  const declaredLength = Number(request.headers.get("Content-Length"));
  if (Number.isFinite(declaredLength) && declaredLength > MAX_BODY_BYTES) {
    return errorResponse(413, "request_too_large", "Request body is too large.");
  }

  let rawBody;
  try {
    rawBody = await request.text();
  } catch {
    return errorResponse(400, "unreadable_json", "Request body could not be read.");
  }
  if (new TextEncoder().encode(rawBody).byteLength > MAX_BODY_BYTES) {
    return errorResponse(413, "request_too_large", "Request body is too large.");
  }

  let payload;
  try {
    payload = JSON.parse(rawBody);
  } catch {
    return errorResponse(400, "invalid_json", "Request body must be valid JSON.");
  }
  if (!hasExactFields(payload)) {
    return errorResponse(
      400,
      "invalid_fields",
      "Exactly language, question, and session are required.",
    );
  }

  const {language, question, session} = payload;
  if (typeof language !== "string" || !ALLOWED_LANGUAGES.has(language)) {
    return errorResponse(400, "unsupported_language", "Initial live languages are ru and en.");
  }
  if (typeof session !== "string" || !SESSION_PATTERN.test(session)) {
    return errorResponse(400, "invalid_session", "Session must be an ephemeral opaque value.");
  }
  if (typeof question !== "string") {
    return errorResponse(400, "invalid_question", "Question must be text.");
  }

  const normalizedQuestion = question.trim();
  if (!normalizedQuestion) {
    return errorResponse(400, "empty_question", "Question must not be empty.");
  }
  if (Array.from(normalizedQuestion).length > MAX_QUESTION_CHARACTERS) {
    return errorResponse(413, "question_too_long", "Question is too long.");
  }
  if (CONTROL_PATTERN.test(normalizedQuestion)) {
    return errorResponse(400, "control_characters", "Question contains control characters.");
  }
  if (URL_PATTERN.test(normalizedQuestion)) {
    return errorResponse(400, "url_retrieval_disabled", "URL retrieval is not available.");
  }

  if (!groundingIsReady()) {
    return errorResponse(503, "grounding_unavailable", "Public grounding is unavailable.");
  }

  return jsonResponse(503, {
    decision: "refuse",
    language,
    answer: DISABLED_MESSAGE[language],
    citations: [],
    refusal_category: "service_unavailable",
  });
}


export function onRequestPost(context) {
  return handleRequest(context.request);
}


export function onRequest(context) {
  return handleRequest(context.request);
}
