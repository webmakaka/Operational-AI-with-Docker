/**
 * nodejs_sdk.js — Call Docker Model Runner using the openai npm package.
 *
 * Install: npm install openai
 * Run:     node nodejs_sdk.js
 *
 * When your Node app runs inside a Docker container (e.g. via Compose),
 * use model-runner.docker.internal instead of localhost.
 */

const OpenAI = require("openai");

// From host machine use localhost:12434.
// From inside a container (Compose) use model-runner.docker.internal.
const isInContainer = process.env.RUNNING_IN_CONTAINER === "true";
const baseURL = isInContainer
  ? "http://model-runner.docker.internal/engines/v1"
  : "http://localhost:12434/engines/v1";

const client = new OpenAI({
  baseURL,
  apiKey: "not-required", // DMR ignores the API key
});

async function main() {
  const completion = await client.chat.completions.create({
    model: "ai/smollm2:360M-Q4_K_M",
    messages: [{ role: "user", content: "What is Docker Compose?" }],
  });

  console.log(completion.choices[0].message.content);
  console.log(`\nTokens used: ${completion.usage.total_tokens}`);
}

main().catch(console.error);
