import assert from "node:assert/strict";
import {
  RATE_LIMIT_POLICY,
  handleRateLimitRequest,
} from "./src/index.js";


function request({method = "POST", key = RATE_LIMIT_POLICY.key, path = "/limit"} = {}) {
  return new Request(`https://public-ai-rate-limiter.internal${path}`, {
    method,
    headers: {"X-Public-AI-Rate-Limit-Key": key},
  });
}


const tests = [];
function addTest(name, run) {
  tests.push({name, run});
}


addTest("policy is conservative and non-public", async () => {
  assert.equal(RATE_LIMIT_POLICY.binding, "PUBLIC_AI_RATE_LIMITER");
  assert.equal(RATE_LIMIT_POLICY.key, "public-ai:/api/ai/ask");
  assert.equal(RATE_LIMIT_POLICY.limit, 2);
  assert.equal(RATE_LIMIT_POLICY.periodSeconds, 60);
  assert.equal(RATE_LIMIT_POLICY.publicRoutesEnabled, false);
});

addTest("only the internal limit operation is accepted", async () => {
  assert.equal((await handleRateLimitRequest(request({path: "/"}))).status, 404);
  assert.equal((await handleRateLimitRequest(request({method: "GET"}))).status, 405);
  assert.equal((await handleRateLimitRequest(request({key: "wrong"}))).status, 403);
});

addTest("missing binding fails closed", async () => {
  assert.equal((await handleRateLimitRequest(request())).status, 503);
});

addTest("binding failure and malformed output fail closed", async () => {
  const throwing = {
    PUBLIC_AI_RATE_LIMITER: {limit: async () => { throw new Error("offline"); }},
  };
  const malformed = {
    PUBLIC_AI_RATE_LIMITER: {limit: async () => ({})},
  };
  assert.equal((await handleRateLimitRequest(request(), throwing)).status, 503);
  assert.equal((await handleRateLimitRequest(request(), malformed)).status, 503);
});

addTest("rejected admission returns 429", async () => {
  let capturedKey;
  const env = {
    PUBLIC_AI_RATE_LIMITER: {
      limit: async ({key}) => {
        capturedKey = key;
        return {success: false};
      },
    },
  };
  const response = await handleRateLimitRequest(request(), env);
  assert.equal(response.status, 429);
  assert.equal(response.headers.get("Retry-After"), "60");
  assert.equal(capturedKey, RATE_LIMIT_POLICY.key);
});

addTest("admitted request returns empty 204", async () => {
  const env = {
    PUBLIC_AI_RATE_LIMITER: {limit: async () => ({success: true})},
  };
  const response = await handleRateLimitRequest(request(), env);
  assert.equal(response.status, 204);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
  assert.equal(await response.text(), "");
});


let failures = 0;
for (const test of tests) {
  try {
    await test.run();
    process.stdout.write(`Rate-limit Worker test PASS: ${test.name}\n`);
  } catch (error) {
    failures += 1;
    process.stderr.write(`Rate-limit Worker test FAIL: ${test.name}\n${error.stack}\n`);
  }
}

if (failures) process.exit(1);
process.stdout.write(`Rate-limit Worker tests PASS: ${tests.length}/${tests.length}.\n`);
