import itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 15
RAM_MAX = 16.0
CPU_MAX = 8.0
POP_SIZE = 60
GENERATIONS = 100
TOURNAMENT_K = 3
P_CROSS = 0.9
P_MUT = 1.0 / N
ELITE = 1
ALPHA = 1.5
RUNS = 30

_rng = np.random.default_rng(7)
VALUE = _rng.integers(10, 101, size=N).astype(float)
RAM = np.round(_rng.uniform(1.0, 6.0, size=N) * 2) / 2
CPU = np.round(_rng.uniform(0.5, 2.5, size=N) * 2) / 2


def totals(ind):
    return float(ind @ VALUE), float(ind @ RAM), float(ind @ CPU)


def feasible(ind):
    _, r, c = totals(ind)
    return r <= RAM_MAX and c <= CPU_MAX


def fitness_hard(ind):
    v, r, c = totals(ind)
    if r > RAM_MAX or c > CPU_MAX:
        return 0.0
    return v


def fitness_proportional(ind):
    v, r, c = totals(ind)
    viol = max(0.0, r - RAM_MAX) / RAM_MAX + max(0.0, c - CPU_MAX) / CPU_MAX
    return max(0.0, v * (1.0 - ALPHA * viol))


def tournament(pop, fit, rng):
    idx = rng.integers(0, len(pop), size=TOURNAMENT_K)
    return pop[idx[np.argmax(fit[idx])]].copy()


def crossover(a, b, rng):
    if rng.random() < P_CROSS:
        pt = int(rng.integers(1, N))
        return np.concatenate([a[:pt], b[pt:]]), np.concatenate([b[:pt], a[pt:]])
    return a.copy(), b.copy()


def mutate(ind, rng):
    mask = rng.random(N) < P_MUT
    ind[mask] = 1 - ind[mask]
    return ind


def diversity(pop):
    n = len(pop)
    s = pop.sum(axis=0)
    pairs_diff = s * (n - s)
    return float(pairs_diff.sum() / (N * n * (n - 1) / 2))


class BinaryGA:
    def __init__(self, fitness_fn, seed):
        self.fitness_fn = fitness_fn
        self.rng = np.random.default_rng(seed)

    def run(self):
        rng = self.rng
        pop = rng.integers(0, 2, size=(POP_SIZE, N))
        best_feasible = None
        best_feasible_v = -1.0
        log = {"mean": [], "std": [], "div": [], "feas": [], "best_fit": []}
        for _ in range(GENERATIONS + 1):
            fit = np.array([self.fitness_fn(i) for i in pop])
            feas = np.array([feasible(i) for i in pop])
            for i in np.where(feas)[0]:
                v = totals(pop[i])[0]
                if v > best_feasible_v:
                    best_feasible_v = v
                    best_feasible = pop[i].copy()
            log["mean"].append(fit.mean())
            log["std"].append(fit.std())
            log["div"].append(diversity(pop))
            log["feas"].append(feas.mean())
            log["best_fit"].append(fit.max())
            order = np.argsort(-fit)
            new = [pop[j].copy() for j in order[:ELITE]]
            while len(new) < POP_SIZE:
                p1 = tournament(pop, fit, rng)
                p2 = tournament(pop, fit, rng)
                c1, c2 = crossover(p1, p2, rng)
                new.append(mutate(c1, rng))
                if len(new) < POP_SIZE:
                    new.append(mutate(c2, rng))
            pop = np.array(new)
        top = pop[np.argmax([self.fitness_fn(i) for i in pop])]
        log["final_top_feasible"] = feasible(top)
        return best_feasible, best_feasible_v, {k: np.array(v) if isinstance(v, list) else v for k, v in log.items()}


def brute_force():
    best_v = -1.0
    best = None
    for bits in itertools.product([0, 1], repeat=N):
        ind = np.array(bits)
        if feasible(ind):
            v = totals(ind)[0]
            if v > best_v:
                best_v = v
                best = ind
    return best, best_v


def main():
    opt, opt_v = brute_force()
    strategies = {"A (Penalidade Rígida)": fitness_hard, "B (Penalidade Proporcional)": fitness_proportional}
    out = {}
    for name, fn in strategies.items():
        logs = []
        bests = []
        bvals = []
        infeasible_top = 0
        for r in range(RUNS):
            ga = BinaryGA(fn, seed=500 + r)
            b, bv, log = ga.run()
            logs.append(log)
            bests.append(b)
            bvals.append(bv)
            if not log["final_top_feasible"]:
                infeasible_top += 1
        agg = {k: np.mean([l[k] for l in logs], axis=0) for k in ["mean", "std", "div", "feas", "best_fit"]}
        agg["mean_sd"] = np.std([l["mean"] for l in logs], axis=0)
        bvals = np.array(bvals)
        b = int(np.argmax(bvals))
        out[name] = {
            "agg": agg,
            "best": bests[b],
            "best_v": bvals[b],
            "vals": bvals,
            "hit_opt": int(np.sum(bvals >= opt_v)),
            "infeasible_top": infeasible_top,
        }

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for name, o in out.items():
        a = o["agg"]
        x = np.arange(GENERATIONS + 1)
        axes[0, 0].plot(x, a["mean"], label=name)
        axes[0, 0].fill_between(x, a["mean"] - a["mean_sd"], a["mean"] + a["mean_sd"], alpha=0.15)
        axes[0, 1].plot(x, a["std"], label=name)
        axes[1, 0].plot(x, a["div"], label=name)
        axes[1, 1].plot(x, 100 * a["feas"], label=name)
    axes[0, 0].axhline(opt_v, color="k", ls="--", lw=1, label=f"ótimo global = {opt_v:.0f}")
    axes[0, 0].set_title("Fitness médio da população (30 execuções ± dp entre execuções)")
    axes[0, 1].set_title("Desvio-padrão do fitness dentro da população")
    axes[1, 0].set_title("Diversidade genética (distância de Hamming média normalizada)")
    axes[1, 1].set_title("% de indivíduos viáveis na população")
    for ax in axes.ravel():
        ax.set_xlabel("Geração")
        ax.grid(alpha=0.3)
        ax.legend()
    plt.tight_layout()
    plt.savefig("lab02_comparacao.png", dpi=130)

    L = []
    L.append("Dados dos 15 microsserviços (gerados com seed=7, pois o enunciado não os fornece):")
    L.append("")
    L.append("| Serviço | Valor | RAM (GB) | CPU (cores) |")
    L.append("|---|---|---|---|")
    for i in range(N):
        L.append(f"| S{i + 1} | {VALUE[i]:.0f} | {RAM[i]:.1f} | {CPU[i]:.1f} |")
    L.append("")
    L.append(f"Ótimo global por força bruta (2^15 combinações): valor = {opt_v:.0f}, serviços = {[f'S{i + 1}' for i in np.where(opt == 1)[0]]}, RAM = {totals(opt)[1]:.1f}, CPU = {totals(opt)[2]:.1f}")
    L.append("")
    L.append(f"Parâmetros: população {POP_SIZE}, {GENERATIONS} gerações, torneio k={TOURNAMENT_K}, cruzamento 1 ponto pc={P_CROSS}, mutação pm=1/{N}, elitismo {ELITE}, alpha(B)={ALPHA}, {RUNS} execuções independentes.")
    L.append("")
    L.append("| Estratégia | Melhor valor viável (melhor execução) | Média±dp dos melhores (30 exec.) | Execuções que acharam o ótimo | Execuções cujo melhor da população final era inviável | Melhor combinação |")
    L.append("|---|---|---|---|---|---|")
    for name, o in out.items():
        sv = [f"S{i + 1}" for i in np.where(o["best"] == 1)[0]]
        t = totals(o["best"])
        L.append(f"| {name} | {o['best_v']:.0f} | {o['vals'].mean():.1f} ± {o['vals'].std():.1f} | {o['hit_opt']}/{RUNS} | {o['infeasible_top']}/{RUNS} | {sv} (RAM {t[1]:.1f}, CPU {t[2]:.1f}) |")
    L.append("")
    L.append("| Geração | A: média | A: dp | A: diversidade | A: % viáveis | B: média | B: dp | B: diversidade | B: % viáveis |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    ka, kb = list(out.keys())
    for g in [0, 10, 25, 50, 75, 100]:
        a = out[ka]["agg"]
        b = out[kb]["agg"]
        L.append(f"| {g} | {a['mean'][g]:.1f} | {a['std'][g]:.1f} | {a['div'][g]:.3f} | {100 * a['feas'][g]:.0f}% | {b['mean'][g]:.1f} | {b['std'][g]:.1f} | {b['div'][g]:.3f} | {100 * b['feas'][g]:.0f}% |")
    L.append("")
    for name, o in out.items():
        L.append(f"Diversidade média ao longo das gerações, {name}: {o['agg']['div'].mean():.3f}")
    text = "\n".join(L)
    open("out_lab02.md", "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
