# tiny-chess-v3e

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/0xfari/tiny-chess-v3e/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/0xfari/tiny-chess-v3e/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

tiny-chess v3e — per-game reset + neutral contempt vs weak rungs (4 KB)

v3b core (PeSTO eval, alpha-beta/PVS/LMR/NMP, 1.49x speed work, incremental
eval, capture-only quiescence gen, fast ordering, per-scenario node budget)
+ two directed changes, both motivated by the v3b/v3c trial record:

- Contempt games 1-2 neutralised: CT -50/-40 -> 0/0. Per-rung record over
  3 trials each: games 1-2 scored v2 4.0 pts, v3b 3.0, v3c 4.0 — v3b's hard
  contempt vs the two weakest rungs cost a full point, and v3c's softer
  -20/-15 recovered it. v3e takes the neutral value v2 itself used there.
- Per-game TT/H reset: at a game's first move (fewer than 11 distinct
  positions in the replayed history) the transposition table and history
  heuristic are cleared. Why: v3c trial 1 collapsed on games 3, 6, 7 with
  settings IDENTICAL to v3b — the only cross-game channel is persistent
  TT/KL/H state, so an early game's play can cascade into later games.
  Killer moves are intentionally NOT cleared (a stale killer only matters
  if it coincides with a legal move). The TT-overflow guard (>400k) is kept.

- Games 3-8 keep v3b's table exactly (NODES 150k/150k/120k/60k/40k/40k,
  CT 0/+25/+35/+45/+45/+45).

`src.py` is the readable source; `main.py` is packed with the kit
`makefun compress` (4,090 bytes, cap 4,096). See EVIDENCE.md.

Local practice grades (kit v7, half-CPU): mean Elo 1441 (1530 / 1396 / 1396),
13.0 pts/24 vs v2's 1301 / 10.0 pts. Max think 5.97 s (limit 10 s), zero
timeout losses. Full numbers in EVIDENCE.md.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5tm223q&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
