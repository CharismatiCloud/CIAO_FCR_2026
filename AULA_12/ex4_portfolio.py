import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class PortfolioProblem(ElementwiseProblem):
    def __init__(self):
        # x1: % Renda Fixa, x2: % Ações. Restrição de investimento: rf + acoes <= 100 (sem alavancagem)
        super().__init__(n_var=2, n_obj=2, n_ieq_constr=1, xl=np.array([0.0, 0.0]), xu=np.array([100.0, 100.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        rf, acoes = x[0], x[1]
        f1_retorno_negativo = -(rf * 0.08 + acoes * 0.18)
        f2_risco = rf * 0.02 + acoes * 0.25
        out["F"] = [f1_retorno_negativo, f2_risco]
        out["G"] = [rf + acoes - 100.0]

res4 = minimize(PortfolioProblem(), NSGA2(pop_size=40), termination=('n_gen', 60), seed=1, verbose=False)
risco, retorno = res4.F[:, 1], -res4.F[:, 0]
print(f"Soluções na fronteira: {len(res4.F)}")
i = np.argsort(risco)
for k in i[[0, len(i)//2, -1]]:
    print(f"RF={res4.X[k,0]:.1f}% Ações={res4.X[k,1]:.1f}% -> risco={risco[k]:.2f} | retorno={retorno[k]:.2f}")

plt.figure(figsize=(7, 4))
plt.scatter(risco, retorno, color='orange', s=45)
plt.title("Exercício 4 — Risco vs. Retorno"); plt.xlabel("Risco [Minimizar]"); plt.ylabel("Retorno esperado [Maximizar]")
plt.grid(True); plt.savefig("ex4_pareto.png", dpi=120, bbox_inches="tight")
