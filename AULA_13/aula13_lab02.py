import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize


class KubernetesClusterProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Replicas da API (2 a 40), x2: Worker Nodes (1 a 12)
        super().__init__(n_var=2, n_obj=2, xl=np.array([2, 1]), xu=np.array([40, 12]), vtype=int)

    def _evaluate(self, x, out, *args, **kwargs):
        replicas, nodes = x[0], x[1]
        f1_tempo = (600.0 / replicas) + (200.0 / nodes)     # ms
        f2_custo = (replicas * 12.0) + (nodes * 85.0)       # USD/mês
        out["F"] = [f1_tempo, f2_custo]


algorithm = NSGA2(
    pop_size=25,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True,
)

res2 = minimize(KubernetesClusterProblem(), algorithm, termination=('n_gen', 35), seed=10, verbose=False)

print(f"Solucoes na fronteira: {len(res2.F)}")
print("Replicas | Nodes | Tempo (ms) | Custo (USD/mes)")
for x, f in sorted(zip(res2.X, res2.F), key=lambda t: t[1][1]):
    print(f"{int(x[0]):8d} | {int(x[1]):5d} | {f[0]:10.2f} | {f[1]:8.2f}")
