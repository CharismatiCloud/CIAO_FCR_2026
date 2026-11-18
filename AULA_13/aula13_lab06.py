import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize
from pymoo.mcdm.pseudo_weights import PseudoWeights


class EscalaHospitalarProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Medicos Plantonistas (2 a 20), x2: Enfermeiros (4 a 40)
        super().__init__(n_var=2, n_obj=2, n_ieq_constr=1,
                         xl=np.array([2, 4]), xu=np.array([20, 40]), vtype=int)

    def _evaluate(self, x, out, *args, **kwargs):
        medicos, enfermeiros = x[0], x[1]
        f1_custo = (medicos * 1200.0) + (enfermeiros * 450.0)
        f2_espera = (180.0 / medicos) + (240.0 / enfermeiros)
        g1 = f2_espera - 25.0          # SLA: espera <= 25 min  ->  g1 <= 0
        out["F"] = [f1_custo, f2_espera]
        out["G"] = [g1]


algorithm = NSGA2(
    pop_size=40,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True,
)

res6 = minimize(EscalaHospitalarProblem(), algorithm, termination=('n_gen', 50), seed=42, verbose=False)

# Somente solucoes viaveis (CV <= 0)
viavel = res6.CV[:, 0] <= 0
X, F = res6.X[viavel], res6.F[viavel]
print(f"Solucoes viaveis na fronteira: {len(F)} de {len(res6.F)}")
print("Medicos | Enfermeiros | Custo (R$) | Espera (min)")
for x, f in sorted(zip(X, F), key=lambda t: t[1][0]):
    print(f"{int(x[0]):7d} | {int(x[1]):11d} | {f[0]:10.2f} | {f[1]:8.2f}")

i = PseudoWeights(np.array([0.40, 0.60])).do(F)
x_ok, f_ok = X[i], F[i]
print("\nEscala recomendada (pesos 40% Custo / 60% Tempo de Espera):")
print(f"-> Medicos: {int(x_ok[0])} | Enfermeiros: {int(x_ok[1])}")
print(f"-> Custo do plantao: R$ {f_ok[0]:.2f} | Tempo de espera: {f_ok[1]:.2f} min")
assert f_ok[1] <= 25.0, "Solucao escolhida viola o SLA de 25 min"
print(f"Restricao f2_espera <= 25.0 respeitada: {f_ok[1]:.2f} <= 25.0")
