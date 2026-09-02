const LIMIT_PATH = "/limit";
const RATE_LIMIT_KEY = "public-ai:/api/ai/ask";


function emptyResponse(status, headers = {}) {
  return new Response(null, {
    status,
    headers: {
      "Cache-Control": "no-store",
      ...headers,
    },
  });
}


export async function handleRateLimitRequest(request, env = {}) {
  const url = new URL(request.url);
  if (url.pathname !== LIMIT_PATH) return emptyResponse(404);
  if (request.method !== "POST") {
    return emptyResponse(405, {Allow: "POST"});
  }
  if (request.headers.get("X-Public-AI-Rate-Limit-Key") !== RATE_LIMIT_KEY) {
    return emptyResponse(403);
  }
  if (!env.PUBLIC_AI_RATE_LIMITER || typeof env.PUBLIC_AI_RATE_LIMITER.limit !== "function") {
    return emptyResponse(503);
  }

  let result;
  try {
    result = await env.PUBLIC_AI_RATE_LIMITER.limit({key: RATE_LIMIT_KEY});
  } catch {
    return emptyResponse(503);
  }
  if (!result || typeof result.success !== "boolean") return emptyResponse(503);
  if (!result.success) return emptyResponse(429, {"Retry-After": "60"});
  return emptyResponse(204);
}


export default {
  fetch(request, env) {
    return handleRateLimitRequest(request, env);
  },
};


export const RATE_LIMIT_POLICY = Object.freeze({
  binding: "PUBLIC_AI_RATE_LIMITER",
  key: RATE_LIMIT_KEY,
  limit: 2,
  periodSeconds: 60,
  publicRoutesEnabled: false,
});
