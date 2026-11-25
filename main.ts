import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
// Guard: the file must really be a PNG (magic bytes), not a misnamed JPEG.
const head = readFileSync(src).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!head.equals(pngMagic)) throw new Error("entry.png is not a PNG");
copyFileSync(src, dst);
const bytes = statSync(dst).size;
if (bytes > 1048576) throw new Error(`entry.png too large: ${bytes} bytes`);
console.log(`entry.png copied (${bytes} bytes)`);
