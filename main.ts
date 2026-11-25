// news-image-20261125 — main.ts (Node 22, standard library only).
//
// The entry image is the entry.png vendored beside this file. The program
// copies it to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when the
// variable is unset), creating the output directory first. No network, no
// randomness: two runs write identical bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
