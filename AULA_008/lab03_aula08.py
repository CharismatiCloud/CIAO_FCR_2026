import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 10
RHO = 0.2
ALPHA = 1.0
BETA = 3.0
N_ANTS = 30
ITERATIONS = 100
TOP_K = 3
Q = 100.0
RUNS = 20
N_RANDOM = 2000

_rng = np.random.default_rng(11)
COORDS = _rng.uniform(0, 100, size=(N, 2))
D = np.round(np.linalg.norm(COORDS[:, None, :] - COORDS[None, :, :], axis=2), 1)
EDGES = [(i, j) for i in range(N) for j in range(i + 1, N)]


class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.p[ra] = rb
        return True


def tree_cost(tree):
    return float(sum(D[i, j] for i, j in tree))


def is_valid_tree(tree):
    if len(tree) != N - 1:
        return False
    uf = UnionFind(N)
    for i, j in tree:
        if not uf.union(i, j):
            return False
    return len({uf.find(x) for x in range(N)}) == 1


def random_tree(rng):
    order = rng.permutation(len(EDGES))
    uf = UnionFind(N)
    tree = []
    for k in order:
        i, j = EDGES[k]
        if uf.union(i, j):
            tree.append((i, j))
        if len(tree) == N - 1:
            break
    return tree


def mst_prim():
    in_tree = {0}
    tree = []
    while len(in_tree) < N:
        best = None
        for i in in_tree:
            for j in range(N):
                if j not in in_tree and (best is None or D[i, j] < D[best[0], best[1]]):
                    best = (i, j)
        tree.append((min(best), max(best)))
        in_tree.add(best[1])
    return tree


def adjacency(tree):
    A = np.zeros((N, N), dtype=int)
    for i, j in tree:
        A[i, j] = A[j, i] = 1
    return A


class AntColonyTree:
    def __init__(self, evaporation_mode, seed):
        self.mode = evaporation_mode
        self.rng = np.random.default_rng(seed)
        self.tau = np.ones((N, N))
        self.eta = np.zeros((N, N))
        mask = D > 0
        self.eta[mask] = 1.0 / D[mask]

    def build(self):
        uf = UnionFind(N)
        tree = []
        cand = list(range(len(EDGES)))
        for _ in range(N - 1):
            valid = [k for k in cand if uf.find(EDGES[k][0]) != uf.find(EDGES[k][1])]
            w = np.array([(self.tau[EDGES[k]] ** ALPHA) * (self.eta[EDGES[k]] ** BETA) for k in valid])
            p = w / w.sum()
            k = valid[int(self.rng.choice(len(valid), p=p))]
            i, j = EDGES[k]
            uf.union(i, j)
            tree.append((i, j))
            cand.remove(k)
        return tree

    def update(self, ranked):
        top = ranked[:TOP_K]
        if self.mode == "global":
            self.tau *= (1.0 - RHO)
        else:
            touched = set()
            for _, t in top:
                touched.update(t)
            for i, j in touched:
                self.tau[i, j] *= (1.0 - RHO)
                self.tau[j, i] = self.tau[i, j]
        for cost, t in top:
            for i, j in t:
                self.tau[i, j] += Q / cost
                self.tau[j, i] = self.tau[i, j]
        self.tau = np.maximum(self.tau, 1e-6)

    def run(self):
        best_tree = None
        best_cost = np.inf
        history = []
        for _ in range(ITERATIONS):
            ants = []
            for _ in range(N_ANTS):
                t = self.build()
                ants.append((tree_cost(t), t))
            ants.sort(key=lambda x: x[0])
            if ants[0][0] < best_cost:
                best_cost, best_tree = ants[0]
            history.append(best_cost)
            self.update(ants)
        return best_tree, best_cost, np.array(history)


def main():
    mst = mst_prim()
    mst_cost = tree_cost(mst)
    rng = np.random.default_rng(99)
    rand_costs = np.array([tree_cost(random_tree(rng)) for _ in range(N_RANDOM)])
    single_random = random_tree(np.random.default_rng(2024))
    single_cost = tree_cost(single_random)

    res = {}
    for mode in ["best_only", "global"]:
        costs = []
        hists = []
        trees = []
        for r in range(RUNS):
            aco = AntColonyTree(mode, seed=300 + r)
            t, c, h = aco.run()
            assert is_valid_tree(t)
            costs.append(c)
            hists.append(h)
            trees.append(t)
        costs = np.array(costs)
        b = int(np.argmin(costs))
        res[mode] = {"costs": costs, "hist": np.array(hists), "best_tree": trees[b], "best_cost": costs[b]}

    main_mode = "best_only"
    aco_tree = res[main_mode]["best_tree"]
    aco_cost = res[main_mode]["best_cost"]
    A = adjacency(aco_tree)

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for mode, label in [("best_only", "Evaporação só nas melhores topologias (enunciado)"), ("global", "Evaporação global (ACO clássico)")]:
        h = res[mode]["hist"]
        x = np.arange(1, ITERATIONS + 1)
        ax[0].plot(x, h.mean(axis=0), label=label)
        ax[0].fill_between(x, h.mean(axis=0) - h.std(axis=0), h.mean(axis=0) + h.std(axis=0), alpha=0.15)
    ax[0].axhline(mst_cost, color="k", ls="--", lw=1, label=f"MST (ótimo) = {mst_cost:.1f}")
    ax[0].axhline(rand_costs.mean(), color="r", ls=":", lw=1, label=f"Média aleatória = {rand_costs.mean():.1f}")
    ax[0].set_xlabel("Iteração")
    ax[0].set_ylabel("Melhor latência total acumulada")
    ax[0].set_title("Convergência do ACO (20 execuções)")
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=0.3)
    ax[1].scatter(COORDS[:, 0], COORDS[:, 1], s=200, c="tab:blue", zorder=3)
    for i in range(N):
        ax[1].text(COORDS[i, 0], COORDS[i, 1], str(i), color="w", ha="center", va="center", zorder=4)
    for i, j in aco_tree:
        ax[1].plot([COORDS[i, 0], COORDS[j, 0]], [COORDS[i, 1], COORDS[j, 1]], "k-", zorder=2)
    ax[1].set_title(f"Topologia final do ACO (latência = {aco_cost:.1f})")
    ax[1].set_aspect("equal")
    plt.tight_layout()
    plt.savefig("lab03_aco.png", dpi=130)

    def gain(base, val):
        return 100.0 * (base - val) / base

    L = []
    L.append("Matriz de latências D (10x10, gerada a partir de coordenadas com seed=11, pois o enunciado não a fornece):")
    L.append("")
    L.append("```")
    L.append(np.array2string(D, formatter={"float_kind": lambda x: f"{x:6.1f}"}, max_line_width=200))
    L.append("```")
    L.append("")
    L.append(f"Parâmetros: rho={RHO}, alpha={ALPHA}, beta={BETA}, {N_ANTS} formigas, {ITERATIONS} iterações, deposita as {TOP_K} melhores, Q={Q}, {RUNS} execuções.")
    L.append("")
    L.append("Matriz de Adjacência final (ACO, evaporação só nas melhores topologias):")
    L.append("")
    L.append("```")
    L.append(np.array2string(A, max_line_width=200))
    L.append("```")
    L.append("")
    L.append(f"Arestas: {[(int(i), int(j)) for i, j in sorted(aco_tree)]}, nº de arestas = {len(aco_tree)}, árvore válida = {is_valid_tree(aco_tree)}")
    L.append("")
    L.append("| Método | Latência total |")
    L.append("|---|---|")
    L.append(f"| MST (Prim, ótimo exato) | {mst_cost:.1f} |")
    for mode, lab in [("best_only", "ACO evaporação só nas melhores (enunciado)"), ("global", "ACO evaporação global (clássico)")]:
        c = res[mode]["costs"]
        L.append(f"| {lab}: melhor / média±dp | {c.min():.1f} / {c.mean():.1f} ± {c.std():.1f} (ótimo em {int(np.sum(c <= mst_cost + 1e-9))}/{RUNS} execuções) |")
    L.append(f"| Topologia aleatória única (seed 2024) | {single_cost:.1f} |")
    L.append(f"| Topologias aleatórias ({N_RANDOM}): média±dp / melhor | {rand_costs.mean():.1f} ± {rand_costs.std():.1f} / {rand_costs.min():.1f} |")
    L.append("")
    L.append("| Comparação | Ganho de redução de latência |")
    L.append("|---|---|")
    L.append(f"| ACO (melhor) vs topologia aleatória única | {gain(single_cost, aco_cost):.2f}% |")
    L.append(f"| ACO (melhor) vs média de {N_RANDOM} aleatórias | {gain(rand_costs.mean(), aco_cost):.2f}% |")
    L.append(f"| ACO (média das {RUNS} exec.) vs média de {N_RANDOM} aleatórias | {gain(rand_costs.mean(), res[main_mode]['costs'].mean()):.2f}% |")
    L.append(f"| ACO global (média) vs média aleatórias | {gain(rand_costs.mean(), res['global']['costs'].mean()):.2f}% |")
    L.append(f"| Gap do ACO (melhor) para o MST | {max(0.0, 100.0 * (aco_cost - mst_cost) / mst_cost):.2f}% |")
    text = "\n".join(L)
    open("out_lab03.md", "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
