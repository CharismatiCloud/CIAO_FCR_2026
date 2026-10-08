import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0])
T_LIMIT = 75.0
K_LOAD = 1.5
PENALTY = 100.0
POPS = [10, 30, 50]
ITERATIONS = 100
RUNS = 30


def normalize(x):
    x = np.clip(x, 0.0, None)
    s = x.sum()
    if s <= 1e-12:
        return np.full_like(x, 1.0 / len(x))
    return x / s


def temperatures(w, model):
    if model == "linear":
        return C.copy()
    return C * (1.0 + K_LOAD * w)


def mean_temperature(w, model):
    return float(np.dot(w, temperatures(w, model)))


def make_fitness(model, counter):
    def fitness(w):
        t = temperatures(w, model)
        excess = np.maximum(0.0, t - T_LIMIT)
        counter["evals"] += 1
        if excess.any():
            counter["violations"] += 1
        return float(np.dot(w, t)) + PENALTY * float(np.sum(excess ** 2))
    return fitness


class PSO:
    def __init__(self, n_particles, dim, fitness_fn, inertia=0.72, c1=1.49, c2=1.49, vmax=0.25, seed=0):
        self.n = n_particles
        self.dim = dim
        self.fitness_fn = fitness_fn
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.vmax = vmax
        self.rng = np.random.default_rng(seed)

    def run(self, iterations):
        rng = self.rng
        pos = rng.dirichlet(np.ones(self.dim), size=self.n)
        vel = rng.uniform(-0.1, 0.1, size=(self.n, self.dim))
        pbest = pos.copy()
        pbest_f = np.array([self.fitness_fn(p) for p in pos])
        g = int(np.argmin(pbest_f))
        gbest = pbest[g].copy()
        gbest_f = float(pbest_f[g])
        history = [gbest_f]
        for _ in range(iterations):
            r1 = rng.random((self.n, self.dim))
            r2 = rng.random((self.n, self.dim))
            vel = self.inertia * vel + self.c1 * r1 * (pbest - pos) + self.c2 * r2 * (gbest - pos)
            vel = np.clip(vel, -self.vmax, self.vmax)
            pos = pos + vel
            pos = np.apply_along_axis(normalize, 1, pos)
            f = np.array([self.fitness_fn(p) for p in pos])
            improved = f < pbest_f
            pbest[improved] = pos[improved]
            pbest_f[improved] = f[improved]
            g = int(np.argmin(pbest_f))
            if pbest_f[g] < gbest_f:
                gbest_f = float(pbest_f[g])
                gbest = pbest[g].copy()
            history.append(gbest_f)
        return gbest, gbest_f, np.array(history)


def reference_optimum():
    f = lambda w: mean_temperature(w, "load")
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    res = minimize(f, np.full(6, 1 / 6), method="SLSQP", bounds=[(0, 1)] * 6, constraints=cons)
    return res.x, res.fun


def main():
    ref_w, ref_f = reference_optimum()
    results = {}
    for n in POPS:
        hists = []
        finals = []
        ws = []
        counter = {"evals": 0, "violations": 0}
        fit = make_fitness("load", counter)
        for r in range(RUNS):
            pso = PSO(n, 6, fit, seed=1000 * n + r)
            w, fv, h = pso.run(ITERATIONS)
            hists.append(h)
            finals.append(fv)
            ws.append(w)
        hists = np.array(hists)
        finals = np.array(finals)
        b = int(np.argmin(finals))
        results[n] = {
            "hist_mean": hists.mean(axis=0),
            "hist_std": hists.std(axis=0),
            "best_w": ws[b],
            "best_f": finals[b],
            "mean_f": finals.mean(),
            "std_f": finals.std(),
            "viol_rate": counter["violations"] / counter["evals"],
            "best_maxT": float(temperatures(ws[b], "load").max()),
        }

    counter = {"evals": 0, "violations": 0}
    lin = PSO(30, 6, make_fitness("linear", counter), seed=7)
    lw, lf, lh = lin.run(ITERATIONS)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for n in POPS:
        m = results[n]["hist_mean"]
        s = results[n]["hist_std"]
        x = np.arange(len(m))
        axes[0].plot(x, m, label=f"{n} partículas")
        axes[0].fill_between(x, m - s, m + s, alpha=0.15)
        axes[1].plot(x, m, label=f"{n} partículas")
    axes[0].axhline(ref_f, color="k", ls="--", lw=1, label="ótimo de referência (SLSQP)")
    axes[0].set_title("Evolução do fitness (média de 30 execuções ± desvio)")
    axes[0].set_xlabel("Iteração")
    axes[0].set_ylabel("Melhor fitness (°C ponderado)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    axes[1].axhline(ref_f, color="k", ls="--", lw=1)
    axes[1].set_xlim(0, 40)
    lo = ref_f - 0.05
    axes[1].set_ylim(lo, lo + 1.5)
    axes[1].set_title("Zoom nas 40 primeiras iterações")
    axes[1].set_xlabel("Iteração")
    axes[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("lab01_fitness.png", dpi=130)

    lines = []
    lines.append(f"Ótimo de referência (SLSQP, só para validação): fitness = {ref_f:.4f}, W = {np.round(ref_w, 4).tolist()}")
    lines.append("")
    lines.append("| População | w1 | w2 | w3 | w4 | w5 | w6 | sum(wi) | Fitness (melhor) | Média±dp (30 execuções) | Tmax AZ | % avaliações com violação |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for n in POPS:
        r = results[n]
        w = r["best_w"]
        cells = " | ".join(f"{v:.4f}" for v in w)
        lines.append(f"| {n} | {cells} | {w.sum():.10f} | {r['best_f']:.4f} | {r['mean_f']:.4f} ± {r['std_f']:.4f} | {r['best_maxT']:.2f} | {100 * r['viol_rate']:.1f}% |")
    lines.append("")
    lines.append("Modelo literal (temperatura = coeficiente C, sem efeito de carga), 30 partículas:")
    lines.append(f"W = {np.round(lw, 4).tolist()}, sum = {lw.sum():.10f}, fitness = {lf:.4f}, violações = {counter['violations']}")
    lines.append("")
    lines.append("Fitness médio por iteração (marcos):")
    lines.append("")
    lines.append("| Iteração | 10 | 30 | 50 |")
    lines.append("|---|---|---|---|")
    for it in [0, 5, 10, 20, 50, 100]:
        lines.append(f"| {it} | " + " | ".join(f"{results[n]['hist_mean'][it]:.4f}" for n in POPS) + " |")
    text = "\n".join(lines)
    open("out_lab01.md", "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
