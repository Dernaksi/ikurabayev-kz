import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {randomUUID} from "node:crypto";


const contract = JSON.parse(await readFile(
  new URL("../data/public-ai-contract.json", import.meta.url),
  "utf8",
));
const endpoint = process.env.PUBLIC_AI_PILOT_URL;
const token = process.env.AI_PILOT_TOKEN;
const rounds = Number.parseInt(process.env.PUBLIC_AI_EVAL_ROUNDS || "3", 10);
const intervalMs = Number.parseInt(process.env.PUBLIC_AI_EVAL_INTERVAL_MS || "31000", 10);
const caseFilter = process.env.PUBLIC_AI_EVAL_CASE || "";

assert.match(endpoint || "", /^https:\/\/[^/]+\/api\/ai\/ask$/);
assert.ok(token && token.length >= 32, "AI_PILOT_TOKEN must be supplied without printing it");
assert.ok(Number.isInteger(rounds) && rounds >= 1 && rounds <= 5);
assert.ok(Number.isInteger(intervalMs) && intervalMs >= 30_000);

const cases = contract.evaluation_cases.filter(({id}) => !caseFilter || id === caseFilter);
assert.ok(cases.length, "No evaluation cases matched PUBLIC_AI_EVAL_CASE");
const origin = new URL(endpoint).origin;
const results = [];

function sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function validateCase(testCase, language, body) {
  if (body?.decision !== testCase.expected_decision || body?.language !== language) return false;
  if (testCase.expected_decision === "refuse") {
    return body.refusal_category === testCase.refusal_category
      && Array.isArray(body.citations)
      && body.citations.length === 0;
  }
  const citedClaims = new Set((body.citations || []).map(({claim_id}) => claim_id));
  return testCase.required_claim_ids.every((claimId) => citedClaims.has(claimId));
}

for (let round = 1; round <= rounds; round += 1) {
  for (const testCase of cases) {
    for (const language of ["ru", "en"]) {
      const startedAt = performance.now();
      let response;
      let body;
      try {
        response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Origin: origin,
            "X-Pilot-Token": token,
          },
          body: JSON.stringify({
            language,
            question: testCase.prompts[language],
            session: randomUUID(),
          }),
        });
        body = await response.json();
      } catch {
        response = {status: 0, headers: new Headers()};
        body = null;
      }
      const latencyMs = Math.round(performance.now() - startedAt);
      const passed = response.status === 200 && validateCase(testCase, language, body);
      const result = {
        case_id: testCase.id,
        decision: body?.decision || "transport_failure",
        input_tokens: Number(response.headers.get("X-AI-Pilot-Input-Tokens")) || null,
        language,
        latency_ms: latencyMs,
        model: response.headers.get("X-AI-Pilot-Model") || "unknown",
        output_tokens: Number(response.headers.get("X-AI-Pilot-Output-Tokens")) || null,
        passed,
        round,
        status: response.status,
      };
      results.push(result);
      console.log(JSON.stringify(result));
      const isFinalCall = round === rounds
        && testCase === cases.at(-1)
        && language === "en";
      if (!isFinalCall) await sleep(intervalMs);
    }
  }
}

const passed = results.filter((result) => result.passed).length;
const summary = {
  attempts: results.length,
  failed: results.length - passed,
  passed,
  pass_rate: passed / results.length,
};
console.log(`Public AI private-pilot evaluation summary: ${JSON.stringify(summary)}`);
process.exitCode = passed === results.length ? 0 : 1;
