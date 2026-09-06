import assert from "node:assert/strict";
import {
  PublicAiRateLimiter,
  RATE_LIMIT_POLICY,
  handleRateLimitRequest,
} from "./src/index.js";


function request({method = "POST", key = RATE_LIMIT_POLICY.key, path = "/limit"} = {}) {
  return new Request(`https://public-ai-rate-limiter.internal${path}`, {
    method,
    headers: {"X-Public-AI-Rate-Limit-Key": key},
  });
}


function createState() {
  const values = new Map();
  const storage = {
    async get(key) { return values.get(key); },
    async put(key, value) { values.set(key, structuredClone(value)); },
    async transaction(callback) { return callback(storage); },
  };
  return {storage};
}


function durableObjectNamespace(object) {
  return {
    idFromName(name) { return name; },
    get() { return object; },
  };
}


const tests = [];
function addTest(name, run) {
  tests.push({name, run});
}


addTest("policy is strict, global, and non-public", async () => {
  assert.equal(RATE_LIMIT_POLICY.durableObjectBinding, "PUBLIC_AI_LIMITER");
  assert.equal(RATE_LIMIT_POLICY.durableObjectClass, "PublicAiRateLimiter");
  assert.equal(RATE_LIMIT_POLICY.key, "public-ai:/api/ai/ask");
  assert.equal(RATE_LIMIT_POLICY.limit, 5);
  assert.equal(RATE_LIMIT_POLICY.periodSeconds, 60);
  assert.equal(RATE_LIMIT_POLICY.algorithm, "strict_global_rolling_window");
  assert.equal(RATE_LIMIT_POLICY.storesRequestContent, false);
  assert.equal(RATE_LIMIT_POLICY.storesClientIdentifier, false);
  assert.equal(RATE_LIMIT_POLICY.publicRoutesEnabled, false);
});

addTest("only the internal limit operation is accepted", async () => {
  assert.equal((await handleRateLimitRequest(request({path: "/"}))).status, 404);
  assert.equal((await handleRateLimitRequest(request({method: "GET"}))).status, 405);
  assert.equal((await handleRateLimitRequest(request({key: "wrong"}))).status, 403);
});

addTest("missing, throwing, and malformed Durable Object bindings fail closed", async () => {
  const throwing = {
    PUBLIC_AI_LIMITER: {
      idFromName: () => "id",
      get: () => ({fetch: async () => { throw new Error("offline"); }}),
    },
  };
  const malformed = {
    PUBLIC_AI_LIMITER: {idFromName: () => "id", get: () => ({fetch: async () => ({})})},
  };
  assert.equal((await handleRateLimitRequest(request())).status, 503);
  assert.equal((await handleRateLimitRequest(request(), throwing)).status, 503);
  assert.equal((await handleRateLimitRequest(request(), malformed)).status, 503);
});

addTest("Durable Object strictly rejects the sixth request in its rolling window", async () => {
  let now = 1_000_000;
  const object = new PublicAiRateLimiter(createState(), {}, () => now);
  const admission = () => object.fetch(request({path: "/admit"}));
  for (let index = 0; index < 5; index += 1) {
    assert.equal((await admission()).status, 204);
  }
  const rejected = await admission();
  assert.equal(rejected.status, 429);
  assert.equal(rejected.headers.get("Retry-After"), "60");
  now += 59_999;
  assert.equal((await admission()).status, 429);
  now += 1;
  assert.equal((await admission()).status, 204);
});

addTest("gateway forwards admission and bounded retry information", async () => {
  const object = new PublicAiRateLimiter(createState());
  const env = {PUBLIC_AI_LIMITER: durableObjectNamespace(object)};
  for (let index = 0; index < 5; index += 1) {
    assert.equal((await handleRateLimitRequest(request(), env)).status, 204);
  }
  const response = await handleRateLimitRequest(request(), env);
  assert.equal(response.status, 429);
  assert.match(response.headers.get("Retry-After"), /^([1-9]|[1-5][0-9]|60)$/);
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
