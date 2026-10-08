# ==============================================================================
# AULA 09 — SPRINT 1 (AC-3): MODELAGEM DAS VARIÁVEIS E CONJUNTO FUZZY
# Ventilador fuzzy com scikit-fuzzy
# ==============================================================================
import matplotlib
import os, warnings
warnings.filterwarnings("ignore", message=".*non-interactive.*")
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(PASTA, exist_ok=True)   # cria a pasta img ao lado do .py
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1) VARIÁVEIS: entrada (temperatura) e saída (velocidade do ventilador)
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), "temperatura")
velocidade = ctrl.Consequent(np.arange(0, 101, 1), "velocidade")

# 2) CONJUNTOS FUZZY  (trapmf = [a,b,c,d] | trimf = [a,b,c])
temperatura["frio"] = fuzz.trapmf(temperatura.universe, [0, 0, 15, 25])
temperatura["morno"] = fuzz.trimf(temperatura.universe, [15, 25, 35])
temperatura["quente"] = fuzz.trapmf(temperatura.universe, [25, 35, 40, 40])

velocidade["baixa"] = fuzz.trimf(velocidade.universe, [0, 0, 50])
velocidade["media"] = fuzz.trimf(velocidade.universe, [0, 50, 100])
velocidade["alta"] = fuzz.trimf(velocidade.universe, [50, 100, 100])

# 3) REGRAS: SE ... ENTÃO ...
regras = [
    ctrl.Rule(temperatura["frio"], velocidade["baixa"]),
    ctrl.Rule(temperatura["morno"], velocidade["media"]),
    ctrl.Rule(temperatura["quente"], velocidade["alta"]),
]

# 4) SISTEMA DE CONTROLE
sistema = ctrl.ControlSystem(regras)
ventilador = ctrl.ControlSystemSimulation(sistema)

print("Temperatura -> pertinências (frio/morno/quente) -> velocidade")
for temp in [10, 20, 25, 30, 38]:
    ventilador.input["temperatura"] = temp
    ventilador.compute()
    mu = {n: float(fuzz.interp_membership(temperatura.universe, temperatura[n].mf, temp))
          for n in ("frio", "morno", "quente")}
    print(f"{temp:>2}°C | frio={mu['frio']:.2f} morno={mu['morno']:.2f} "
          f"quente={mu['quente']:.2f} -> ventilador a {ventilador.output['velocidade']:.0f}%")

# 5) GRÁFICOS (salvos em PNG)
temperatura.view(); plt.savefig(os.path.join(PASTA, "lab01_temperatura.png"), dpi=130, bbox_inches="tight")
velocidade.view();  plt.savefig(os.path.join(PASTA, "lab01_velocidade.png"), dpi=130, bbox_inches="tight")

# Curva de resposta completa (entrada x saída)
ts = np.arange(0, 40.5, 0.5); saidas = []
for t in ts:
    ventilador.input["temperatura"] = t
    ventilador.compute()
    saidas.append(ventilador.output["velocidade"])
plt.figure(figsize=(7, 4))
plt.plot(ts, saidas, lw=2)
plt.xlabel("Temperatura (°C)"); plt.ylabel("Velocidade (%)")
plt.title("Superfície de resposta do ventilador fuzzy"); plt.grid(alpha=.3)
plt.savefig(os.path.join(PASTA, "lab01_resposta.png"), dpi=130, bbox_inches="tight")

# Defuzzificação ilustrada para 30 °C
ventilador.input["temperatura"] = 30
ventilador.compute()
velocidade.view(sim=ventilador)
plt.savefig(os.path.join(PASTA, "lab01_defuzz_30C.png"), dpi=130, bbox_inches="tight")