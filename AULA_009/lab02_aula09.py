"""
AULA 09 — Laboratório 2: Gorjeta fuzzy com scikit-fuzzy (+ experimentos 1 a 5)
Execução: python lab02_aula09.py   (Enter nas perguntas usa os valores padrão 7 e 3)
"""
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


def construir(regra2="servico", mf="tri", metodo="centroid", excelente=False):
    """Monta o sistema. Parâmetros permitem fazer os experimentos."""
    servico = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "servico")
    comida = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "comida")
    gorjeta = ctrl.Consequent(np.arange(0, 25.01, 0.5), "gorjeta", defuzzify_method=metodo)

    for nome, var in (("servico", servico), ("comida", comida)):
        if nome == "servico" and mf == "trap":
            var["ruim"] = fuzz.trapmf(var.universe, [0, 0, 1, 5])
            var["medio"] = fuzz.trapmf(var.universe, [2, 4, 6, 8])
            var["bom"] = fuzz.trapmf(var.universe, [5, 9, 10, 10])
        elif nome == "servico" and mf == "gauss":
            var["ruim"] = fuzz.gaussmf(var.universe, 0, 2)
            var["medio"] = fuzz.gaussmf(var.universe, 5, 2)
            var["bom"] = fuzz.gaussmf(var.universe, 10, 2)
        elif nome == "servico" and excelente:
            var["ruim"] = fuzz.trimf(var.universe, [0, 0, 3])
            var["medio"] = fuzz.trimf(var.universe, [0, 3.5, 7])
            var["bom"] = fuzz.trimf(var.universe, [3.5, 7, 10])
            var["excelente"] = fuzz.trimf(var.universe, [7, 10, 10])
        else:
            var["ruim"] = fuzz.trimf(var.universe, [0, 0, 5])
            var["medio"] = fuzz.trimf(var.universe, [0, 5, 10])
            var["bom"] = fuzz.trimf(var.universe, [5, 10, 10])

    gorjeta["baixa"] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
    gorjeta["media"] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
    gorjeta["alta"] = fuzz.trimf(gorjeta.universe, [13, 25, 25])

    r2 = servico["medio"] if regra2 == "servico" else servico["medio"] & comida["medio"]
    regras = [
        ctrl.Rule(servico["ruim"] | comida["ruim"], gorjeta["baixa"]),
        ctrl.Rule(r2, gorjeta["media"]),
        ctrl.Rule(servico["bom"] | comida["bom"], gorjeta["alta"]),
    ]
    if excelente:
        regras.append(ctrl.Rule(servico["excelente"], gorjeta["alta"]))
    return servico, comida, gorjeta, ctrl.ControlSystemSimulation(ctrl.ControlSystem(regras))


def calcular(sim, s, c):
    sim.input["servico"] = s
    sim.input["comida"] = c
    sim.compute()
    return float(sim.output["gorjeta"])


def pedir_nota(texto, padrao):
    try:
        resposta = input(f"{texto} (0-10) [{padrao}]: ").strip()
    except EOFError:
        resposta = ""
    return float(resposta.replace(",", ".")) if resposta else padrao


if __name__ == "__main__":
    servico, comida, gorjeta, sim = construir()
    s = pedir_nota("Nota do serviço", 7)
    c = pedir_nota("Nota da comida", 3)
    print(f"\n=> Gorjeta sugerida: {calcular(sim, s, c):.1f}%")

    servico.view();  plt.savefig(os.path.join(PASTA, "lab02_servico.png"), dpi=130, bbox_inches="tight")
    comida.view();   plt.savefig(os.path.join(PASTA, "lab02_comida.png"), dpi=130, bbox_inches="tight")
    gorjeta.view(sim=sim); plt.savefig(os.path.join(PASTA, "lab02_gorjeta_centroide.png"), dpi=130, bbox_inches="tight")

    print("\n================ EXPERIMENTOS ================")
    # Exp 1
    base = calcular(construir()[3], 7, 3)
    e1 = calcular(construir(regra2="and")[3], 7, 3)
    print(f"Exp1  regra2 'servico medio' = {base:.2f}% | regra2 'medio & medio' = {e1:.2f}%")
    # Exp 2
    for mf in ("tri", "trap", "gauss"):
        print(f"Exp2  servico={mf:5s} -> (7,3) = {calcular(construir(mf=mf)[3], 7, 3):.2f}%")
    sv, _, _, _ = construir(mf="trap"); sv.view(); plt.savefig(os.path.join(PASTA, "lab02_exp2_trap.png"), dpi=130, bbox_inches="tight")
    sv, _, _, _ = construir(mf="gauss"); sv.view(); plt.savefig(os.path.join(PASTA, "lab02_exp2_gauss.png"), dpi=130, bbox_inches="tight")
    # Exp 3
    for m in ("centroid", "bisector", "mom", "som", "lom"):
        print(f"Exp3  defuzz={m:8s} -> (7,3) = {calcular(construir(metodo=m)[3], 7, 3):.2f}%")
    # Exp 4
    sim4 = construir(excelente=True)[3]
    print(f"Exp4  com 'excelente' -> (7,3) = {calcular(sim4, 7, 3):.2f}% | (10,3) = {calcular(sim4, 10, 3):.2f}%")
    sv, _, _, _ = construir(excelente=True); sv.view(); plt.savefig(os.path.join(PASTA, "lab02_exp4_excelente.png"), dpi=130, bbox_inches="tight")
    # Exp 5
    sim5 = construir()[3]
    for par in [(0, 0), (10, 10), (5, 5)]:
        print(f"Exp5  {par} -> {calcular(sim5, *par):.2f}%")