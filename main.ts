// Entry for "Promote make.fun's make-your-own-bounty post on X".
//
// The post itself is the entry, so this program has one small job:
// carry POST.json from the repository into /output, where the gate
// reads the post's address from it. Nothing written here is scored;
// the house reads the post's replies, reposts and quotes from X.
//
// Local check, mirroring the grader's layout:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

// Inside the grader these point at /bot and /output; locally the
// environment overrides them to the repo root and a scratch folder.
const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (error) {
  console.error(`could not copy POST.json out of ${botDir}: ${(error as Error).message}`);
  process.exit(1);
}

// The gate refuses a POST.json it cannot parse, so fail loudly here
// instead of handing the grader a broken file.
const copied = JSON.parse(readFileSync(target, "utf8")) as unknown;
if (
  typeof copied !== "object" ||
  copied === null ||
  typeof (copied as { url?: unknown }).url !== "string"
) {
  console.error("POST.json has no url string after copying");
  process.exit(1);
}
