const LIMIT_PATH = "/limit";
const ADMIT_PATH = "/admit";
const RATE_LIMIT_KEY = "public-ai:/api/ai/ask";
const LIMITER_OBJECT_NAME = "public-ai-global";
const LIMIT = 5;
const WINDOW_MS = 60_000;


function emptyResponse(status, headers = {}) {
  return new Response(null, {
    status,
    headers: {
      "Cache-Control": "no-store",
      ...headers,
    },
  });
}


function validAdmissions(value, now) {
  if (!Array.isArray(value)) return [];
  return value.filter((timestamp) => (
    Number.isSafeInteger(timestamp)
    && timestamp <= now
    && timestamp > now - WINDOW_MS
  ));
}


export class PublicAiRateLimiter {
  constructor(state, _env, clock = () => Date.now()) {
    this.state = state;
    this.clock = clock;
  }

  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname !== ADMIT_PATH) return emptyResponse(404);
    if (request.method !== "POST") return emptyResponse(405, {Allow: "POST"});
    if (request.headers.get("X-Public-AI-Rate-Limit-Key") !== RATE_LIMIT_KEY) {
      return emptyResponse(403);
    }

    return this.state.storage.transaction(async (storage) => {
      const now = this.clock();
      const admissions = validAdmissions(await storage.get("admissions"), now);
      if (admissions.length >= LIMIT) {
        await storage.put("admissions", admissions);
        const retryAfter = Math.max(1, Math.ceil((admissions[0] + WINDOW_MS - now) / 1_000));
        return emptyResponse(429, {"Retry-After": String(retryAfter)});
      }
      admissions.push(now);
      await storage.put("admissions", admissions);
      return emptyResponse(204);
    });
  }
}


function limiterStub(env) {
  if (!env.PUBLIC_AI_LIMITER || typeof env.PUBLIC_AI_LIMITER.idFromName !== "function") {
    return null;
  }
  const id = env.PUBLIC_AI_LIMITER.idFromName(LIMITER_OBJECT_NAME);
  if (typeof env.PUBLIC_AI_LIMITER.get !== "function") return null;
  const stub = env.PUBLIC_AI_LIMITER.get(id);
  return stub && typeof stub.fetch === "function" ? stub : null;
}


export async function handleRateLimitRequest(request, env = {}) {
  const url = new URL(request.url);
  if (url.pathname !== LIMIT_PATH) return emptyResponse(404);
  if (request.method !== "POST") return emptyResponse(405, {Allow: "POST"});
  if (request.headers.get("X-Public-AI-Rate-Limit-Key") !== RATE_LIMIT_KEY) {
    return emptyResponse(403);
  }

  const stub = limiterStub(env);
  if (!stub) return emptyResponse(503);
  let response;
  try {
    response = await stub.fetch(new Request("https://public-ai-limiter.internal/admit", {
      method: "POST",
      headers: {"X-Public-AI-Rate-Limit-Key": RATE_LIMIT_KEY},
    }));
  } catch {
    return emptyResponse(503);
  }
  if (!(response instanceof Response)) return emptyResponse(503);
  if (response.status === 204) return emptyResponse(204);
  if (response.status === 429) {
    const retryAfter = response.headers.get("Retry-After");
    return emptyResponse(429, retryAfter ? {"Retry-After": retryAfter} : {});
  }
  return emptyResponse(503);
}


export default {
  fetch(request, env) {
    return handleRateLimitRequest(request, env);
  },
};


export const RATE_LIMIT_POLICY = Object.freeze({
  durableObjectBinding: "PUBLIC_AI_LIMITER",
  durableObjectClass: "PublicAiRateLimiter",
  objectName: LIMITER_OBJECT_NAME,
  key: RATE_LIMIT_KEY,
  limit: LIMIT,
  periodSeconds: WINDOW_MS / 1_000,
  algorithm: "strict_global_rolling_window",
  storesRequestContent: false,
  storesClientIdentifier: false,
  publicRoutesEnabled: false,
});
