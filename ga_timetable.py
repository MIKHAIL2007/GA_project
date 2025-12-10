import random

W = {1: 16, 2: 8, 3: 4, 4: 2, 5: 1}

def read_crs(p):
    ex = []
    sz = []
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            a = line.split()
            ex.append(a[0])
            if len(a) > 1:
                try:
                    sz.append(int(a[1]))
                except:
                    sz.append(0)
            else:
                sz.append(0)
    return ex, sz

def read_stu(p):
    rs = []
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rs.append(line.split())
    return rs

def build_idx(ex):
    d = {}
    for i, e in enumerate(ex):
        d[e] = i
    return d

def build_st(rs, ix):
    st = []
    for s in rs:
        xs = []
        for e in s:
            if e in ix:
                xs.append(ix[e])
        seen = set()
        xs2 = []
        for a in xs:
            if a not in seen:
                seen.add(a)
                xs2.append(a)
        if xs2:
            st.append(xs2)
    return st

def build_conf(rs, ix, n):
    ad = [set() for _ in range(n)]
    for s in rs:
        xs = []
        for e in s:
            if e in ix:
                xs.append(ix[e])

        seen = set()
        xs2 = []
        for a in xs:
            if a not in seen:
                seen.add(a)
                xs2.append(a)
        xs = xs2

        m = len(xs)
        for i in range(m):
            a = xs[i]
            for j in range(i + 1, m):
                b = xs[j]
                if a != b:
                    ad[a].add(b)
                    ad[b].add(a)
    return ad

def greedy_seed(ad, t, tries=200):
    n = len(ad)
    deg = []
    for i in range(n):
        deg.append(len(ad[i]))

    for _ in range(tries):
        tmp = []
        for i in range(n):
            tmp.append((deg[i], random.random(), i))
        tmp.sort(reverse=True)

        order = []
        for _, _, i in tmp:
            order.append(i)

        x = [-1] * n
        ok_all = True

        for e in order:
            bad = set()
            for nb in ad[e]:
                s = x[nb]
                if s != -1:
                    bad.add(s)

            placed = False
            for k in range(t):
                if k not in bad:
                    x[e] = k
                    placed = True
                    break

            if not placed:
                ok_all = False
                break

        if ok_all:
            return x

    return None

def fix_g(x, ad, t, passes=2):
    n = len(ad)
    for _ in range(passes):
        for e in range(n):
            s = x[e]
            bad = set()
            for nb in ad[e]:
                bad.add(x[nb])
            if s in bad:
                ok = []
                for k in range(t):
                    if k not in bad:
                        ok.append(k)
                if ok:
                    x[e] = random.choice(ok)
                else:
                    x[e] = random.randrange(t)

def init_pop(ps, ad, t):
    base = greedy_seed(ad, t, tries=300)
    n = len(ad)

    if base is None:
        pop = []
        for _ in range(ps):
            x = [random.randrange(t) for _ in range(n)]
            fix_g(x, ad, t, passes=3)
            pop.append(x)
        return pop

    pop = [base[:]]
    while len(pop) < ps:
        x = base[:]
        for _ in range(3):
            i = random.randrange(n)
            x[i] = random.randrange(t)
        fix_g(x, ad, t, passes=3)
        pop.append(x)

    return pop

def eval_one(x, st):
    c = 0
    p = 0
    for s in st:
        slots = []
        for e in s:
            slots.append(x[e])
        if len(slots) != len(set(slots)):
            c += 1
            continue
        m = len(slots)
        for i in range(m):
            for j in range(i + 1, m):
                d = abs(slots[i] - slots[j])
                if d > 0 and d <= 5:
                    p += W[d]
    return c, p

def fit(x, st, sn):
    c, p = eval_one(x, st)
    if c > 0:
        return -1e6 * c - (p / sn)
    return -(p / sn)

def tour(pop, fs, k):
    ids = random.sample(range(len(pop)), k)
    b = ids[0]
    bf = fs[b]
    for i in ids[1:]:
        if fs[i] > bf:
            bf = fs[i]
            b = i
    return pop[b][:]

def cross(a, b, cx):
    n = len(a)
    if random.random() >= cx:
        return a[:], b[:]
    x = []
    y = []
    for i in range(n):
        if random.random() < 0.5:
            x.append(a[i])
            y.append(b[i])
        else:
            x.append(b[i])
            y.append(a[i])
    return x, y

def mut(x, ad, t, mu):
    n = len(x)
    for i in range(n):
        if random.random() < mu:
            bad = set()
            for nb in ad[i]:
                bad.add(x[nb])
            ok = []
            for k in range(t):
                if k not in bad:
                    ok.append(k)
            if ok:
                x[i] = random.choice(ok)
            else:
                x[i] = random.randrange(t)

def run(crs, stu, t=24, ps=80, g=200, cx=0.8, mu=0.03, k=3, v=True, seed=1, pr=20):
    random.seed(seed)

    ex, _ = read_crs(crs)
    ix = build_idx(ex)
    rs = read_stu(stu)

    st = build_st(rs, ix)
    n = len(ex)
    sn = len(st)

    ad = build_conf(rs, ix, n)

    pop = init_pop(ps, ad, t)

    best = None
    bf = -1e18
    bg = None

    for gen in range(g):
        fs = []
        for x in pop:
            fs.append(fit(x, st, sn))

        bi = 0
        bfi = fs[0]
        for i in range(1, len(pop)):
            if fs[i] > bfi:
                bfi = fs[i]
                bi = i

        if bfi > bf:
            bf = bfi
            best = pop[bi][:]
            bg = gen

        if v and (gen % pr == 0 or gen == g - 1):
            c, p = eval_one(best, st)
            print("gen", gen, "clash_students", c, "best_pen", p / sn)

        new = []
        while len(new) < ps:
            p1 = tour(pop, fs, k)
            p2 = tour(pop, fs, k)
            c1, c2 = cross(p1, p2, cx)

            mut(c1, ad, t, mu)
            mut(c2, ad, t, mu)

            fix_g(c1, ad, t, passes=2)
            fix_g(c2, ad, t, passes=2)

            new.append(c1)
            if len(new) < ps:
                new.append(c2)

        if best is not None and new:
            new[0] = best[:]

        pop = new

    c, p = eval_one(best, st)
    info = {
        "exams": n,
        "students": sn,
        "timeslots": t,
        "best_generation": bg,
        "clash_students": c,
        "total_penalty": p,
        "avg_penalty": (p / sn) if sn else None
    }
    return best, bf, info