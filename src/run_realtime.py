"""Run a requests file through the real-time Messages API (pilot / small runs).

Output: results/raw/{name}.jsonl, one line per custom_id. Resumable: done ids are skipped.
Usage: python src/run_realtime.py --name pilot
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import RAW_DIR, REQUESTS_DIR, CostMeter, load_jsonl, make_client, response_text


def call(client, meter, req):
    msg = client.messages.create(**req["params"])
    meter.add(req["params"]["model"], msg.usage)
    return {
        "custom_id": req["custom_id"],
        "model": req["params"]["model"],
        "text": response_text(msg),
        "stop_reason": msg.stop_reason,
        "input_tokens": msg.usage.input_tokens,
        "output_tokens": msg.usage.output_tokens,
        "source": "realtime",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--mock", action="store_true")
    args = ap.parse_args()

    reqs = load_jsonl(REQUESTS_DIR / f"{args.name}.jsonl")
    if not reqs:
        raise SystemExit("no requests - run src/build_requests.py first")
    out_path = RAW_DIR / f"{args.name}.jsonl"
    done = {r["custom_id"] for r in load_jsonl(out_path)}
    todo = [r for r in reqs if r["custom_id"] not in done]
    print(f"{len(reqs)} requests, {len(done)} done, {len(todo)} to run")

    client, meter, errors = make_client(args.mock), CostMeter(), []
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as out, ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(call, client, meter, r): r for r in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            try:
                row = fut.result()
            except Exception as e:
                errors.append((futs[fut]["custom_id"], repr(e)[:300]))
                continue
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            if i % 100 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)}  {meter.summary()}")

    print(f"-> {out_path}  | this run: {meter.summary()}")
    if errors:
        print(f"{len(errors)} errors (re-run to retry):")
        for e in errors[:5]:
            print("  ", e)


if __name__ == "__main__":
    main()
