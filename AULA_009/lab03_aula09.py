"""
AULA 09 — Lab 3 (Agro): Dose de fertilizante nitrogenado (kg N/ha)
a partir da ACIDEZ DO SOLO (pH) e da FASE DA CULTURA (% do ciclo).
Execução: python lab03_aula09.py
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

# ---------- 1) Universos de discurso ----------
ph = ctrl.Antecedent(np.arange(4.0, 9.01, 0.05), "ph")            # pH (adimensional)
fase = ctrl.Antecedent(np.arange(0, 100.1, 1), "fase")            # % do ciclo da cultura
dose = ctrl.Consequent(np.arange(0, 120.1, 1), "dose")            # kg N/ha

# ---------- 2) Conjuntos fuzzy ----------
# Extremos = trapézio (ombro); termos centrais = triângulo
ph["acido"] = fuzz.trapmf(ph.universe, [4.0, 4.0, 5.0, 5.8])
ph["ideal"] = fuzz.trimf(ph.universe, [5.2, 6.0, 6.8])
ph["alcalino"] = fuzz.trapmf(ph.universe, [6.2, 7.2, 9.0, 9.0])

fase["inicial"] = fuzz.trapmf(fase.universe, [0, 0, 15, 35])
fase["vegetativa"] = fuzz.trimf(fase.universe, [20, 45, 70])
fase["reprodutiva"] = fuzz.trimf(fase.universe, [50, 70, 90])
fase["maturacao"] = fuzz.trapmf(fase.universe, [75, 90, 100, 100])

dose["nula"] = fuzz.trapmf(dose.universe, [0, 0, 5, 20])
dose["baixa"] = fuzz.trimf(dose.universe, [10, 30, 50])
dose["media"] = fuzz.trimf(dose.universe, [40, 65, 90])
dose["alta"] = fuzz.trapmf(dose.universe, [75, 100, 120, 120])

# ---------- 3) Base de regras (| = OU, & = E) ----------
nao_ideal = ph["acido"] | ph["alcalino"]
regras = [
    ctrl.Rule(ph["ideal"] & fase["vegetativa"], dose["alta"]),          # R1
    ctrl.Rule(ph["ideal"] & fase["reprodutiva"], dose["media"]),        # R2
    ctrl.Rule(ph["ideal"] & fase["inicial"], dose["baixa"]),            # R3
    ctrl.Rule(nao_ideal & fase["vegetativa"], dose["media"]),           # R4 (OU + E)
    ctrl.Rule(nao_ideal & fase["inicial"], dose["baixa"]),              # R5
    ctrl.Rule(nao_ideal & fase["reprodutiva"], dose["baixa"]),          # R6
    ctrl.Rule(fase["maturacao"], dose["nula"]),                         # R7
]
sistema = ctrl.ControlSystem(regras)


def calcular(p, f):
    sim = ctrl.ControlSystemSimulation(sistema)
    sim.input["ph"], sim.input["fase"] = p, f
    sim.compute()
    return sim, float(sim.output["dose"])


if __name__ == "__main__":
    # ---------- 4) Testes (entrada, saída, faixa esperada definida ANTES de rodar) ----------
    testes = [
        ("T1", 6.0, 45, (75, 120), "pH ideal + vegetativa -> dose ALTA"),
        ("T2", 4.5, 45, (40, 80), "solo ácido + vegetativa -> dose MÉDIA (aproveitamento reduzido)"),
        ("T3", 6.0, 95, (0, 15), "maturação -> dose NULA"),
        ("T4", 7.8, 10, (15, 45), "solo alcalino + fase inicial -> dose BAIXA"),
        ("T5", 6.0, 10, (15, 45), "pH ideal + fase inicial -> dose BAIXA"),
        ("T6", 5.5, 60, (40, 85), "transição ácido/ideal e veg./reprodutiva -> MÉDIA/ALTA"),
    ]
    print(f"{'ID':<3} {'pH':>4} {'Fase%':>6} {'Saída kg N/ha':>14} {'Esperado':>10}  Status")
    for tid, p, f, (lo, hi), desc in testes:
        sim, d = calcular(p, f)
        print(f"{tid:<3} {p:>4} {f:>6} {d:>14.1f} {f'{lo}-{hi}':>10}  {'OK' if lo <= d <= hi else 'FORA'}  # {desc}")

    # ---------- 5) Gráficos ----------
    ph.view();   plt.savefig(os.path.join(PASTA, "lab03_ph.png"), dpi=130, bbox_inches="tight")
    fase.view(); plt.savefig(os.path.join(PASTA, "lab03_fase.png"), dpi=130, bbox_inches="tight")
    dose.view(); plt.savefig(os.path.join(PASTA, "lab03_dose.png"), dpi=130, bbox_inches="tight")
    sim, _ = calcular(4.5, 45)
    dose.view(sim=sim); plt.savefig(os.path.join(PASTA, "lab03_defuzz_T2.png"), dpi=130, bbox_inches="tight")

    # Superfície de resposta (mapa de calor)
    P = np.arange(4.0, 9.01, 0.25); F = np.arange(0, 100.1, 2.5)
    Z = np.array([[calcular(p, f)[1] for p in P] for f in F])
    plt.figure(figsize=(7, 5))
    im = plt.pcolormesh(P, F, Z, shading="auto", cmap="YlGn")
    plt.colorbar(im, label="Dose (kg N/ha)")
    plt.xlabel("pH do solo"); plt.ylabel("Fase da cultura (% do ciclo)")
    plt.title("Superfície de resposta do sistema fuzzy")
    plt.savefig(os.path.join(PASTA, "lab03_superficie.png"), dpi=130, bbox_inches="tight")