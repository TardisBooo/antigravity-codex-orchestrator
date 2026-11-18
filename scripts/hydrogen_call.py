#!/usr/bin/env python3
"""Call Gemini 4 Hydrogen with a key read from a local key file.

Used by playbook Phase 5 (ledger and docs) and any other Hydrogen step.
The key is read at call time and passed to `gemini-api` through the child
process environment only. It is never printed, logged or written to disk.

Usage:
  python hydrogen_call.py --prompt-file in.md --out out.md [--system "..."]
  python hydrogen_call.py --selftest

Environment overrides:
  PLAYBOOK_KEY_FILE   path to the key file       (default E:\\Workspaces\\key.txt)
  PLAYBOOK_KEY_LABEL  heading above the key      (default "Gemini 4 Hydrogen")
  PLAYBOOK_HYDROGEN_MODEL                        (default gemini-4-hydrogen)
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

DEFAULT_KEY_FILE = r"E:\Workspaces\key.txt"
DEFAULT_LABEL = "Gemini 4 Hydrogen"
DEFAULT_MODEL = "gemini-4-hydrogen"
RETRYABLE = ("503", "429", "high demand", "overloaded", "unavailable", "timeout")


def load_key(path: str, label: str) -> str:
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8", errors="ignore")
    idx = text.rfind(label)
    if idx < 0:
        sys.exit(f"[hydrogen_call] label {label!r} not found in {path}")
    match = re.search(r"AQ\.[A-Za-z0-9_\-.]+", text[idx:])
    if not match:
        sys.exit(f"[hydrogen_call] no AQ.* key found after {label!r} in {path}")
    return match.group(0)


def extract_text(payload: dict) -> str:
    parts = []
    for step in payload.get("steps") or []:
        if step.get("type") != "model_output":
            continue
        for item in step.get("content") or []:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
    return "".join(parts).strip()


def call(prompt: str, system: str, model: str, key: str, retries: int) -> dict:
    env = dict(os.environ, GEMINI_API_KEY=key)
    cmd = ["gemini-api", "generate", "-m", model, "--stdin", "--stream=false", "-o", "json",
           "--body", '{"store": false}']
    if system:
        cmd += ["--system", system]
    last = ""
    for attempt in range(1, retries + 1):
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
            env=env, shell=(os.name == "nt"),
        )
        blob = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode == 0:
            try:
                payload = json.loads(proc.stdout)
            except json.JSONDecodeError:
                last = "unparseable JSON from gemini-api"
            else:
                text = extract_text(payload)
                if text:
                    return {"text": text, "usage": payload.get("usage"), "attempts": attempt}
                last = "empty model output"
        else:
            last = re.sub(r"\s+", " ", blob)[:300]
            if not any(tok in blob.lower() for tok in RETRYABLE):
                break
        wait = min(5 * attempt, 30)
        print(f"[hydrogen_call] attempt {attempt}/{retries} failed: {last[:120]} (retry in {wait}s)", file=sys.stderr)
        time.sleep(wait)
    sys.exit(f"[hydrogen_call] FAILED after {retries} attempts: {last}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file")
    ap.add_argument("--prompt", "-p", help="Inline prompt string")
    ap.add_argument("--out")
    ap.add_argument("--system", default="")
    ap.add_argument("--model", default=None)
    ap.add_argument("--retries", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    key_file = os.environ.get("PLAYBOOK_KEY_FILE", DEFAULT_KEY_FILE)
    label = os.environ.get("PLAYBOOK_KEY_LABEL", DEFAULT_LABEL)
    model = args.model or os.environ.get("PLAYBOOK_HYDROGEN_MODEL", DEFAULT_MODEL)
    key = load_key(key_file, label)

    if args.selftest:
        res = call("Reply with exactly: HYDROGEN_OK", "", model, key, args.retries)
        ok = "HYDROGEN_OK" in res["text"]
        print(json.dumps({"model": model, "ok": ok, "attempts": res["attempts"], "usage": res["usage"]}))
        sys.exit(0 if ok else 1)

    if args.prompt:
        prompt = args.prompt
    elif args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as fh:
            prompt = fh.read()
    else:
        sys.exit("[hydrogen_call] Either --prompt or --prompt-file is required (or use --selftest)")
    res = call(prompt, args.system, model, key, args.retries)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(res["text"])
        print(os.path.abspath(args.out))
    else:
        print(res["text"])


if __name__ == "__main__":
    main()
