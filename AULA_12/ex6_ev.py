import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class EVBatteryProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=2, n_ieq_constr=1, xl=np.array([10.0, 15.0]), xu=np.array([150.0, 45.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        potencia, temp = x[0], x[1]
        f1_tempo_recarga = 3000.0 / potencia
        f2_desgaste_bateria = (potencia ** 1.5) * (temp / 20.0)
        g1 = f2_desgaste_bateria - 1500.0      # desgaste <= 1500  ->  g1 <= 0
        out["F"] = [f1_tempo_recarga, f2_desgaste_bateria]
        out["G"] = [g1]

res6 = minimize(EVBatteryProblem(), NSGA2(pop_size=40), termination=('n_gen', 50), seed=1, verbose=False)
viaveis = res6.F[res6.CV[:, 0] <= 0]
print(f"Soluções viáveis: {len(viaveis)}")
print("tempo_recarga(min) | desgaste")
for f in viaveis[np.argsort(viaveis[:, 0])]:
    print(f"{f[0]:18.2f} | {f[1]:8.2f}")

plt.figure(figsize=(7, 4))
plt.scatter(viaveis[:, 0], viaveis[:, 1], color='teal', s=45)
plt.axhline(1500, color='red', ls='--', label='Limite de desgaste (1500)')
plt.title("Exercício 6 — Pareto com restrição: EV"); plt.xlabel("Tempo de recarga"); plt.ylabel("Desgaste da bateria")
plt.legend(); plt.grid(True); plt.savefig("ex6_pareto.png", dpi=120, bbox_inches="tight")
