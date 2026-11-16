"""Validate v3e (v3b + neutral contempt games 1-2 + per-game TT/H reset +
semantics-preserving golfs: unified att(), e-notation) vs base/v3b:
perft, eval consistency, gen(1) equivalence, u2m/m2u round-trip,
scenario NODES/CT assignment, att() equivalence vs v3b, reset behaviour, bench.
Usage: python3 validate_v3e.py
"""
import importlib.util, os, random, sys, time

os.environ.setdefault("MAKEFUN_ENV_URL", "http://127.0.0.1:1")

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

BASE = "/home/hatch/workspace/makefun/tiny-chess-test/variants/base.py"
V3B = "/home/hatch/workspace/makefun/tiny-chess-v3b/src.py"
V3E = "/home/hatch/workspace/makefun/tiny-chess-v3e/src.py"
B = load(BASE, "base")
V = load(V3B, "v3b")
A = load(V3E, "v3e")

def setup(m, moves=()):
    m.B = m.start(); m.S = [0,15,-1,0,4,116]; m.rep = {}; m.zinit(); m.rep[m.ZK] = 1
    if m is not B:
        m.MG = 0; m.EG = 0; m.PH = 24; m.BW = 2; m.BB = 2
    for a in moves:
        m.make(m.u2m(a))

def legal(m):
    w = m.S[0]; out = []
    for mv in m.gen():
        un = m.make(mv)
        if not m.att(m.S[4] if w == 0 else m.S[5], w ^ 8):
            out.append(mv)
        m.unmake(un)
    return out

def perft(m, d):
    if d == 0: return 1
    n = 0; w = m.S[0]
    for mv in m.gen():
        un = m.make(mv)
        if not m.att(m.S[4] if w == 0 else m.S[5], w ^ 8):
            n += perft(m, d - 1)
        m.unmake(un)
    return n

# 1. perft (v3e only, exact counts)
setup(A)
assert perft(A, 4) == 197281, perft(A, 4)
print("perft startpos d4 = 197281 OK")
setup(A, "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 d2d3".split())
print("perft startpos OK")

# 2. eval consistency vs base over random games + unmake reversibility
R = random.Random(7)
mism = 0
for g in range(30):
    setup(B); setup(A)
    for _ in range(20):
        mv = R.choice(legal(B))
        u = A.m2u(mv)
        b_before = B.ev()
        a_before = A.ev()
        if b_before != a_before:
            mism += 1
            print("EV MISMATCH", b_before, a_before, "game", g)
        un_b = B.make(mv); un_a = A.make(A.u2m(u))
        if B.ev() != A.ev():
            mism += 1
            print("EV MISMATCH after make", B.ev(), A.ev())
        st = (A.MG, A.EG, A.PH, A.BW, A.BB, A.ZK)
        A.unmake(un_a)
        B.unmake(un_b)
        if B.ev() != b_before or A.ev() != a_before:
            mism += 1
            print("EV MISMATCH after unmake", B.ev(), b_before, A.ev(), a_before)
        if R.random() < 0.5:
            break
print(f"eval consistency: {mism} mismatches over 30 random games")

# 3. gen(1) == old capture filter on random positions
mism3 = 0
for _ in range(200):
    setup(B); setup(A)
    for _ in range(R.randint(0, 25)):
        mv = R.choice(legal(B))
        B.make(mv); A.make(A.u2m(A.m2u(mv)))
    old = set()
    for mv in B.gen():
        t = mv >> 7 & 127
        if B.B[t] or mv >> 14 or (B.B[mv & 127] & 7) == 1 and t == B.S[2]:
            old.add(mv)
    new = set(A.gen(1))
    if old != new:
        mism3 += 1
        print("GEN(1) MISMATCH", old ^ new)
print(f"gen(1) equivalence: {mism3} mismatches over 200 positions")

# 4. u2m/m2u round-trip incl. promotions
for a in ["e2e4", "e7e8q", "e7e8r", "e7e8b", "e7e8n", "a7a8q", "g1f3"]:
    assert A.m2u(A.u2m(a)) == a, (a, A.m2u(A.u2m(a)))
print("u2m/m2u round-trip OK (incl. promotions)")

# 5. att() equivalence vs v3b on random positions (unified att() must match exactly)
mism5 = 0
R5 = random.Random(99)
for _ in range(300):
    setup(V); setup(A)
    for _ in range(R5.randint(0, 30)):
        mv = R5.choice(legal(V))
        u = V.m2u(mv)
        V.make(mv); A.make(A.u2m(u))
    for w in (0, 8):
        for ksq in (V.S[4], V.S[5]):
            if V.att(ksq, w) != A.att(ksq, w):
                mism5 += 1
                print("ATT MISMATCH", ksq, w, V.att(ksq, w), A.att(ksq, w))
print(f"att() equivalence vs v3b: {mism5} mismatches over 300 positions x 4 checks")

# 5b. att() equivalence on synthetic king-proximity boards: kings 1-3 squares
# apart in every direction, plus scattered pieces. The unified att() must not
# report a king attacking from 2+ squares away (a one-char bug class:
# `v<3` breaks only for pawn/knight, not king v=6).
mism5b = 0
R5b = random.Random(1234)
squares = [s for s in range(128) if not s & 136]
n5b = 0
for _ in range(300):
    k1 = R5b.choice(squares)
    d = R5b.choice([-17, -16, -15, -1, 1, 15, 16, 17])
    dist = R5b.choice([1, 2, 3])
    k2 = k1 + d * dist
    if k2 & 136 or k2 == k1:
        continue
    extras = []
    for _ in range(R5b.randint(0, 6)):
        q = R5b.choice(squares)
        if q != k1 and q != k2:
            extras.append((q, R5b.choice([1, 2, 3, 4, 5, 9, 10, 11, 12, 13])))
    for m in (V, A):
        m.B = [0] * 128
        m.B[k1] = 6; m.B[k2] = 14
        for q, p in extras:
            m.B[q] = p
        m.S = [0, 0, -1, 0, k1, k2]
    for sq in (k1, k2, R5b.choice(squares)):
        for w in (0, 8):
            n5b += 1
            if V.att(sq, w) != A.att(sq, w):
                mism5b += 1
                print("ATT SYNTH MISMATCH", sq, w, V.att(sq, w), A.att(sq, w), "kings", k1, k2, "extras", extras)
print(f"att() synthetic king-proximity: {mism5b} mismatches over {n5b} checks")

# 6. scenario NODES/CT assignment (v3e: games 1-2 CT now 0,0)
POS_MOVES = "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 d2d3 d7d6 c2c3".split()
def scenario_check(game, want_nodes, want_ct):
    setup(A, POS_MOVES)
    lm = [A.m2u(mv) for mv in legal(A)]
    A.TT.clear()
    t0 = time.time()
    mv = A.decide({"moves": list(POS_MOVES), "legal_moves": lm, "game": game})
    dt = time.time() - t0
    ok = (A.NODES == want_nodes and A.CT == want_ct and mv in lm)
    print(f"game={game}: NODES={A.NODES} (want {want_nodes}) CT={A.CT} (want {want_ct}) move={mv} {dt:.1f}s {'OK' if ok else 'FAIL'}")
    return ok

allok = True
allok &= scenario_check(1, 40000, 0)
allok &= scenario_check(2, 40000, 0)
allok &= scenario_check(3, 150000, 0)
allok &= scenario_check(4, 150000, 25)
allok &= scenario_check(5, 120000, 35)
allok &= scenario_check(6, 60000, 45)
allok &= scenario_check(7, 40000, 45)
allok &= scenario_check(8, 40000, 45)
A.NODES = 60000
setup(A, POS_MOVES)
lm = [A.m2u(mv) for mv in legal(A)]
A.TT.clear()
mv = A.decide({"moves": list(POS_MOVES), "legal_moves": lm})
print(f"no-opponent: NODES={A.NODES} (want 60000, untouched) move={mv} {'OK' if A.NODES==60000 and mv in lm else 'FAIL'}")
allok &= (A.NODES == 60000)

# 7. per-game reset behaviour (NODES=0 makes the search abort instantly, so the
# reset line's effect is observable in isolation)
OPEN8 = "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6".split()
MID20 = ("e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 e4e5 d7d5 b1a3 f6e4 "
         "c4b3 d4c3 e1g1 c3b2 c1b2").split()
def reset_check(moves, want_cleared):
    setup(A, moves)
    lm = [A.m2u(mv) for mv in legal(A)]
    A.TT["sentinel"] = (1, 2, 3, 4)
    A.KL[0] = 999999
    A.H[5] = 999999
    A.NODES = 0
    mv = A.decide({"moves": list(moves), "legal_moves": lm})
    # v3e clears TT+H per game; KL is intentionally NOT cleared (a stale killer
    # only matters if it coincides with a legal move, so it stays)
    cleared = ("sentinel" not in A.TT and A.H[5] == 0 and A.KL[0] == 999999)
    ok = (cleared == want_cleared) and mv in lm
    print(f"reset moves={len(moves)}: cleared={cleared} (want {want_cleared}) move={mv} {'OK' if ok else 'FAIL'}")
    return ok
allok &= reset_check(OPEN8, True)    # 8 moves: game start -> cleared
allok &= reset_check(MID20, False)   # 20 moves: mid-game -> sentinels survive
# as black: first decide is at 9 moves
OPEN9 = OPEN8 + ["d2d3"]
allok &= reset_check(OPEN9, True)

# 8. bench: v3b vs v3e nps on fixed positions (60k nodes, no game key)
POSITIONS = {
    "startpos": [],
    "g3-mid": "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 e4e5 d7d5 b1a3 f6e4 c4b3 d4c3 e1g1 c3b2 c1b2 c8e6 a3b5 e8g8 b5c3 e4c3 b2c3 f7f6 e5f6 g7f6 a1b1 a7a5".split(),
    "g6-mid": "e2e4 e7e5 g1f3 d7d6 d2d4 g8f6 b1c3 b8d7 c1e3 f6g4 e3g5 f8e7 g5e7 d8e7 c3d5 e7d8 h2h3 g4f6".split(),
    "g5-mid": "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 f3e5 c8e6 e2e4 b7b5 a1b1 b5b4 c3a4 f6e4 f1c4 e6c4 e5c4 d8d5 d1d3 e4d6 c4d6 e7d6 e1g1 d5a2 f1e1".split(),
    "g7-mid": "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 g8f6 b1c3 f8b4 d4c6 b7c6 e4e5 d8e7 c1f4 f6d5 d1d4 d5f4 d4f4 f7f6 a2a3".split(),
}
def bench(m, tag):
    tot_n, tot_t = 0, 0.0
    for name, moves in POSITIONS.items():
        setup(m, moves)
        lm = [m.m2u(mv) for mv in legal(m)]
        m.TT.clear(); m.KL = [0]*1024; m.H = [0]*98304
        m.NODES = 60000
        t0 = time.time()
        mv = m.decide({"moves": list(moves), "legal_moves": lm})
        dt = time.time() - t0
        tot_n += m.nodes; tot_t += dt
        print(f"  {tag} {name}: move={mv} nodes={m.nodes} {dt:.2f}s nps={m.nodes/max(dt,1e-9):.0f}")
    print(f"  {tag} TOTAL nps={tot_n/max(tot_t,1e-9):.0f}")
    return tot_n/max(tot_t,1e-9)
nb = bench(V, "v3b")
ne = bench(A, "v3e")
print(f"bench nps ratio v3e/v3b = {ne/nb:.3f}")

print("ALL OK" if allok and mism == 0 and mism3 == 0 and mism5 == 0 and mism5b == 0 else "FAILURES PRESENT")
