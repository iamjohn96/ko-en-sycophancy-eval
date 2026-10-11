# PROJECT_STATE.md

## Milestones
- [x] D0 10/11 Setup: API key, spend limit, hello call, repo
- [ ] D1 10/12 Data: 300 items, KO translation reviewed
- [ ] D2 10/13 Prompts + 50-item pilot, grader agreement
- [ ] D3 10/14 Main batches submitted (Haiku/Sonnet/Opus)
- [ ] D4 10/15 Results collected, Hermes A/B
- [ ] D5 10/16 Analysis + expansion batch (last submit day)
- [ ] D6 10/17 Report, repo public

## Done
- 2026-10-11: workspace `eval-2026-10` created, API key issued in it
- 2026-10-11: workspace monthly spend limit set to $195
- 2026-10-11: repo skeleton created, pushed to github.com/iamjohn96/ko-en-sycophancy-eval
- 2026-10-11: hello call to claude-haiku-5-5 OK (10 in / 13 out tokens, inference_geo=global)
- 2026-10-11: confirmed billing draws from promo credit (promo $199.99, purchased $0.55 unchanged)

## In progress
(none — D0 complete)

## Decisions
- Repo starts private; made public on D6.

## Batch IDs
(none yet)

## Balance log
| Date | Promo credit left | Note |
| --- | --- | --- |
| 2026-10-11 | $200.00 | before first call |
| 2026-10-11 | $199.99 | after hello call; purchased $0.55 unchanged |

## Issues
- Setup note: never re-run `cp .env.example .env` (it wipes the saved key). hello_haiku.py uses load_dotenv(override=True).

## Next
- Pick source dataset (D1)
