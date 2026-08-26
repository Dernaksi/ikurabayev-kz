import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {
  handleRequest,
} from "../functions/api/ai/ask.js";
import {
  PUBLIC_AI_GROUNDING,
  PUBLIC_AI_GROUNDING_SHA256,
} from "../functions/api/ai/_grounding.js";


const ENDPOINT = "https://ikurabayev.kz/api/ai/ask";
const ORIGIN = "https://ikurabayev.kz";
const SESSION = "public-session-0001";
const tests = [];


function addTest(name, run) {
  tests.push({name, run});
}


function makeRequest(payload, options = {}) {
  const headers = new Headers(options.headers || {});
  if (!options.omitOrigin) headers.set("Origin", options.origin || ORIGIN);
  if (!options.omitContentType) {
    headers.set("Content-Type", options.contentType || "application/json");
  }
  return new Request(ENDPOINT, {
    method: options.method || "POST",
    headers,
    body: options.method === "GET"
      ? undefined
      : (typeof payload === "string" ? payload : JSON.stringify(payload)),
  });
}


async function responseJson(response) {
  return JSON.parse(await response.text());
}


addTest("grounding metadata", async () => {
  assert.match(PUBLIC_AI_GROUNDING_SHA256, /^[a-f0-9]{64}$/);
  assert.equal(PUBLIC_AI_GROUNDING.contract_id, "public-ai-assistant-v0");
  assert.equal(PUBLIC_AI_GROUNDING.claims.length, 25);
  assert.equal(PUBLIC_AI_GROUNDING.relations.length, 39);
  assert.equal(PUBLIC_AI_GROUNDING.sources.length, 15);
  assert.equal(PUBLIC_AI_GROUNDING.topics.length, 8);
});

addTest("GET rejected", async () => {
  const response = await handleRequest(makeRequest(null, {method: "GET"}));
  assert.equal(response.status, 405);
  assert.equal(response.headers.get("Allow"), "POST");
});

addTest("missing origin rejected", async () => {
  const response = await handleRequest(makeRequest({}, {omitOrigin: true}));
  assert.equal(response.status, 403);
  assert.equal((await responseJson(response)).error.code, "same_origin_required");
});

addTest("cross origin rejected", async () => {
  const response = await handleRequest(makeRequest({}, {origin: "https://example.com"}));
  assert.equal(response.status, 403);
});

addTest("non-JSON content rejected", async () => {
  const response = await handleRequest(makeRequest("text", {contentType: "text/plain"}));
  assert.equal(response.status, 415);
  assert.equal((await responseJson(response)).error.code, "json_required");
});

addTest("invalid JSON rejected", async () => {
  const response = await handleRequest(makeRequest("{"));
  assert.equal(response.status, 400);
  assert.equal((await responseJson(response)).error.code, "invalid_json");
});

addTest("extra field rejected", async () => {
  const response = await handleRequest(makeRequest({
    language: "ru",
    question: "Что известно?",
    session: SESSION,
    unexpected: true,
  }));
  assert.equal(response.status, 400);
  assert.equal((await responseJson(response)).error.code, "invalid_fields");
});

addTest("unsupported language rejected", async () => {
  const response = await handleRequest(makeRequest({
    language: "kk",
    question: "Не белгілі?",
    session: SESSION,
  }));
  assert.equal(response.status, 400);
  assert.equal((await responseJson(response)).error.code, "unsupported_language");
});

addTest("invalid session rejected", async () => {
  const response = await handleRequest(makeRequest({
    language: "en",
    question: "What is public?",
    session: "short",
  }));
  assert.equal(response.status, 400);
  assert.equal((await responseJson(response)).error.code, "invalid_session");
});

addTest("oversized question rejected", async () => {
  const response = await handleRequest(makeRequest({
    language: "en",
    question: "x".repeat(601),
    session: SESSION,
  }));
  assert.equal(response.status, 413);
  assert.equal((await responseJson(response)).error.code, "question_too_long");
});

addTest("oversized UTF-8 body rejected before field validation", async () => {
  const response = await handleRequest(makeRequest({
    language: "ru",
    question: "Э".repeat(2050),
    session: SESSION,
  }));
  assert.equal(response.status, 413);
  assert.equal((await responseJson(response)).error.code, "request_too_large");
});

addTest("control characters rejected", async () => {
  const response = await handleRequest(makeRequest({
    language: "en",
    question: "line one\nline two",
    session: SESSION,
  }));
  assert.equal(response.status, 400);
  assert.equal((await responseJson(response)).error.code, "control_characters");
});

addTest("URL retrieval rejected", async () => {
  const response = await handleRequest(makeRequest({
    language: "en",
    question: "Read https://example.com and summarize it",
    session: SESSION,
  }));
  assert.equal(response.status, 400);
  assert.equal((await responseJson(response)).error.code, "url_retrieval_disabled");
});

addTest("valid Russian request fails closed", async () => {
  const response = await handleRequest(makeRequest({
    language: "ru",
    question: "Какие направления исследований представлены?",
    session: SESSION,
  }));
  const body = await responseJson(response);
  assert.equal(response.status, 503);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
  assert.equal(body.decision, "refuse");
  assert.equal(body.language, "ru");
  assert.equal(body.refusal_category, "service_unavailable");
  assert.deepEqual(body.citations, []);
  assert.ok(body.answer.includes("серверную подготовку"));
});

addTest("valid English request fails closed", async () => {
  const response = await handleRequest(makeRequest({
    language: "en",
    question: "What research directions are represented?",
    session: SESSION,
  }));
  const body = await responseJson(response);
  assert.equal(response.status, 503);
  assert.equal(body.decision, "refuse");
  assert.equal(body.language, "en");
  assert.equal(body.refusal_category, "service_unavailable");
  assert.deepEqual(body.citations, []);
  assert.ok(body.answer.includes("server-side preparation"));
});

addTest("backend source has no outbound capability", async () => {
  const source = await readFile(
    new URL("../functions/api/ai/ask.js", import.meta.url),
    "utf8",
  );
  assert.doesNotMatch(source, /\bfetch\s*\(/);
  assert.doesNotMatch(source, /api\.openai\.com/i);
  assert.doesNotMatch(source, /OPENAI_API_KEY/);
  assert.doesNotMatch(source, /\bconsole\.(?:log|info|warn|error)\b/);
  assert.doesNotMatch(source, /localStorage|sessionStorage|document\.cookie/);
});


let failures = 0;
for (const test of tests) {
  try {
    await test.run();
    console.log(`Backend test PASS: ${test.name}`);
  } catch (error) {
    failures += 1;
    console.error(`Backend test FAILED: ${test.name}`);
    console.error(error);
  }
}

if (failures) {
  process.exitCode = 1;
} else {
  console.log(`Public AI backend tests PASS: ${tests.length}/${tests.length}.`);
}
