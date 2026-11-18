import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize


class SOCInteiroProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Pods (1 a 30), x2: Analistas de Nivel 2 (1 a 15) -> ambos inteiros
        super().__init__(n_var=2, n_obj=2, xl=np.array([1, 1]), xu=np.array([30, 15]), vtype=int)

    def _evaluate(self, x, out, *args, **kwargs):
        pods, analistas = x[0], x[1]
        f1_latencia = (400.0 / pods) + (150.0 / analistas)
        f2_custo = (pods * 18.0) + (analistas * 45.0)
        out["F"] = [f1_latencia, f2_custo]


def rodar(inteiro):
    if inteiro:
        alg = NSGA2(
            pop_size=30,
            sampling=IntegerRandomSampling(),
            crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
            mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
            eliminate_duplicates=True,
        )
    else:
        alg = NSGA2(pop_size=30)  # operadores contínuos padrão
    return minimize(SOCInteiroProblem(), alg, termination=('n_gen', 40), seed=42, verbose=False)


res1 = rodar(True)
print("Amostra de 5 solucoes inteiras encontradas (Pods, Analistas):")
for sol_x, sol_f in zip(res1.X[:5], res1.F[:5]):
    print(f"Pods: {int(sol_x[0]):2d} | Analistas: {int(sol_x[1]):2d} => Latencia: {sol_f[0]:6.2f}ms | Custo: R$ {sol_f[1]:6.2f}")

# Comparação prática: variáveis contínuas (sem RoundingRepair) vs. inteiras
res_cont = rodar(False)
print("\nComparacao: operadores continuos padrao (sem IntegerRandomSampling/RoundingRepair)")
for sol_x in res_cont.X[:5]:
    print(f"Pods: {sol_x[0]:8.4f} | Analistas: {sol_x[1]:8.4f}")
print(f"Todas inteiras (continuo)? {bool(np.all(res_cont.X == np.round(res_cont.X)))}")
print(f"Todas inteiras (com RoundingRepair)? {bool(np.all(res1.X == np.round(res1.X)))}")
print(f"Solucoes distintas na fronteira: continuo={len(res_cont.F)} | inteiro={len(res1.F)}")

plt.figure(figsize=(7, 4))
plt.scatter(res1.F[:, 0], res1.F[:, 1], color='teal', s=60, edgecolor='black')
plt.title("Exercicio 1 - Fronteira de Pareto Discreta (Inteiros)")
plt.xlabel("Latencia (ms) [Minimizar]")
plt.ylabel("Custo (R$/h) [Minimizar]")
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("lab01_pareto.png", dpi=120, bbox_inches="tight")
