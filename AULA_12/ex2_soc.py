import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class SOCAllocationProblem(ElementwiseProblem):
    def __init__(self):
        # x1: analistas (1-50), x2: regimento de segurança (1-10); 2 objetivos a minimizar
        super().__init__(n_var=2, n_obj=2, xl=np.array([1.0, 1.0]), xu=np.array([50.0, 10.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        analistas, regimento = x[0], x[1]
        f1_custo = 100.0 * analistas + 50.0 * regimento
        f2_tempo = 200.0 / analistas + 50.0 / regimento
        out["F"] = [f1_custo, f2_tempo]

res2 = minimize(SOCAllocationProblem(), NSGA2(pop_size=30), termination=('n_gen', 40), seed=1, verbose=False)
print(f"Soluções na fronteira: {len(res2.F)}")
i = np.argsort(res2.F[:, 0])
for k in i[[0, len(i)//2, -1]]:
    print(f"analistas={res2.X[k,0]:.2f} regimento={res2.X[k,1]:.2f} -> custo=R$ {res2.F[k,0]:.1f} | tempo={res2.F[k,1]:.2f} min")

plt.figure(figsize=(7, 4))
plt.scatter(res2.F[:, 0], res2.F[:, 1], color='red', s=45)
plt.title("Exercício 2 — Pareto: SOC"); plt.xlabel("Custo (R$)"); plt.ylabel("Tempo de resposta (min)")
plt.grid(True); plt.savefig("ex2_pareto.png", dpi=120, bbox_inches="tight")
