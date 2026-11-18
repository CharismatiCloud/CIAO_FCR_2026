import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.indicators.hv import HV


class RedeSensoresProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Potencia de Transmissao (1 a 100 mW), x2: Intervalo de Envio (1 a 60 s)
        super().__init__(n_var=2, n_obj=2, xl=np.array([1.0, 1.0]), xu=np.array([100.0, 60.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        potencia, intervalo = x[0], x[1]
        f1_consumo_bateria = (potencia * 2.5) + (120.0 / intervalo)
        f2_perda_pacotes = (500.0 / potencia) + (intervalo * 0.8)
        out["F"] = [f1_consumo_bateria, f2_perda_pacotes]


problem = RedeSensoresProblem()

res_curto = minimize(problem, NSGA2(pop_size=40), ('n_gen', 10), seed=42, verbose=False)
res_longo = minimize(problem, NSGA2(pop_size=40), ('n_gen', 80), seed=42, verbose=False)

# Ponto de referencia pior que todas as solucoes
ref_point = np.array([400.0, 600.0])
metrica_hv = HV(ref_point=ref_point)

hv_10_gen = metrica_hv(res_curto.F)
hv_80_gen = metrica_hv(res_longo.F)

print(f"Hipervolume (10 geracoes): {hv_10_gen}")
print(f"Hipervolume (80 geracoes): {hv_80_gen}")
print(f"Ganho do HV: {hv_80_gen - hv_10_gen:.2f} ({(hv_80_gen / hv_10_gen - 1) * 100:.2f}%)")
print(f"Solucoes na fronteira: 10 gen = {len(res_curto.F)} | 80 gen = {len(res_longo.F)}")
