import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class FrotaRobosProblem(ElementwiseProblem):
    def __init__(self):
        # x1: nº de robôs [5, 50]; x2: velocidade média [1.0, 4.0] m/s
        super().__init__(n_var=2, n_obj=2, n_ieq_constr=1, xl=np.array([5.0, 1.0]), xu=np.array([50.0, 4.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        x1, x2 = x[0], x[1]
        f1_custo = x1 * 25.0 + (x2 ** 2) * 8.0          # R$ mil
        f2_tempo = 120.0 / x1 + 40.0 / x2               # minutos
        g1 = x1 * x2 ** 1.5 - 120.0                     # consumo <= 120  ->  g1 <= 0
        out["F"] = [f1_custo, f2_tempo]
        out["G"] = [g1]


if __name__ == "__main__":
    res7 = minimize(FrotaRobosProblem(), NSGA2(pop_size=40), termination=('n_gen', 60), seed=1, verbose=False)
    ok = res7.CV[:, 0] <= 0
    F, X = res7.F[ok], res7.X[ok]
    print(f"Soluções viáveis na fronteira: {len(F)}")

    # Intermediária: mais próxima do ponto ideal (objetivos normalizados)
    Fn = (F - F.min(axis=0)) / (F.max(axis=0) - F.min(axis=0))
    escolhas = {
        "Menor custo": np.argmin(F[:, 0]),
        "Menor tempo": np.argmin(F[:, 1]),
        "Intermediária (trade-off)": np.argmin(np.linalg.norm(Fn, axis=1)),
    }
    for nome, k in escolhas.items():
        consumo = X[k, 0] * X[k, 1] ** 1.5
        print(f"{nome}: robôs={X[k,0]:.2f} vel={X[k,1]:.2f} m/s -> custo=R$ {F[k,0]:.2f} mil | tempo={F[k,1]:.2f} min | consumo={consumo:.1f}")

    plt.figure(figsize=(7, 4.5))
    plt.scatter(F[:, 0], F[:, 1], color='navy', s=45, label='Fronteira de Pareto')
    for nome, k in escolhas.items():
        plt.scatter(F[k, 0], F[k, 1], s=140, marker='*', label=nome, zorder=3)
    plt.title("Exercício 7 — Pareto: Frota de Robôs (AMRs)")
    plt.xlabel("Custo total (R$ mil) [Minimizar]"); plt.ylabel("Tempo de ciclo (min) [Minimizar]")
    plt.legend(); plt.grid(True)
    plt.savefig("ex7_pareto_frota.png", dpi=120, bbox_inches="tight")
    print("Gráfico salvo em ex7_pareto_frota.png")
