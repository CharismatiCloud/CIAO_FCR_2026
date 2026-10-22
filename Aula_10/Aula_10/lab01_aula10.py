"""
AULA 10 - Motor de Inferência Mamdani e Superfície 3D (Sprint 2 da AC-3)
Disciplina: Inteligência Computacional

Sistema fuzzy de priorização de incidentes:
  Entradas : Impacto (0-100 %) e Explorabilidade (0-10)
  Saída    : Urgência (0-100 %)
  Regras   : matriz 3x3 = 9 regras (cobertura total, sem lacunas)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ----------------------------------------------------------------------------
# 1) Construção do sistema
# ----------------------------------------------------------------------------
def construir_sistema(critica="tri", defuzz="centroid"):
    """critica: 'tri' (trimf) ou 'trap' (trapmf)   |   defuzz: 'centroid' ou 'mom'"""
    impacto = ctrl.Antecedent(np.arange(0, 101, 1), "impacto")
    explor = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "explorabilidade")
    urgencia = ctrl.Consequent(np.arange(0, 101, 1), "urgencia", defuzzify_method=defuzz)

    # Entradas (conforme a matriz do enunciado)
    impacto["baixo"] = fuzz.trimf(impacto.universe, [0, 0, 40])
    impacto["medio"] = fuzz.trimf(impacto.universe, [20, 50, 80])
    impacto["alto"] = fuzz.trimf(impacto.universe, [60, 100, 100])

    explor["baixa"] = fuzz.trimf(explor.universe, [0, 0, 4])
    explor["moderada"] = fuzz.trimf(explor.universe, [2, 5, 8])
    explor["alta"] = fuzz.trimf(explor.universe, [6, 10, 10])

    # Saída
    urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 35])
    urgencia["media"] = fuzz.trimf(urgencia.universe, [15, 40, 65])
    urgencia["alta"] = fuzz.trimf(urgencia.universe, [45, 70, 95])
    if critica == "tri":
        urgencia["critica"] = fuzz.trimf(urgencia.universe, [70, 100, 100])
    else:  # trapézio com ombro (platô) na borda superior
        urgencia["critica"] = fuzz.trapmf(urgencia.universe, [70, 90, 100, 100])

    # Matriz de regras 3x3 (9 regras)
    I, E, U = impacto, explor, urgencia
    regras = [
        ctrl.Rule(I["baixo"] & E["baixa"],    U["baixa"]),
        ctrl.Rule(I["baixo"] & E["moderada"], U["baixa"]),
        ctrl.Rule(I["baixo"] & E["alta"],     U["media"]),
        ctrl.Rule(I["medio"] & E["baixa"],    U["media"]),
        ctrl.Rule(I["medio"] & E["moderada"], U["alta"]),
        ctrl.Rule(I["medio"] & E["alta"],     U["alta"]),
        ctrl.Rule(I["alto"]  & E["baixa"],    U["critica"]),
        ctrl.Rule(I["alto"]  & E["moderada"], U["critica"]),
        ctrl.Rule(I["alto"]  & E["alta"],     U["critica"]),
    ]
    return ctrl.ControlSystem(regras), (impacto, explor, urgencia)


def avaliar(sistema, imp, exp):
    sim = ctrl.ControlSystemSimulation(sistema)
    sim.input["impacto"] = imp
    sim.input["explorabilidade"] = exp
    sim.compute()
    return float(sim.output["urgencia"])


def superficie(sistema, n=31):
    xs = np.linspace(0, 100, n)
    ys = np.linspace(0, 10, n)
    Z = np.zeros((n, n))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            Z[i, j] = avaliar(sistema, x, y)
    return xs, ys, Z


def plot_superficie(ax, xs, ys, Z, titulo):
    X, Y = np.meshgrid(xs, ys)
    ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none", alpha=0.95)
    ax.set_xlabel("Impacto (%)")
    ax.set_ylabel("Explorabilidade (0-10)")
    ax.set_zlabel("Urgência (%)")
    ax.set_zlim(0, 100)
    ax.set_title(titulo, fontsize=10)
    ax.view_init(elev=28, azim=-125)


# ----------------------------------------------------------------------------
# 2) Experimento: Centroide x Trapézio x MOM
# ----------------------------------------------------------------------------
CONFIGS = {
    "A0 - Triângulo + Centroide (base)":  ("tri",  "centroid"),
    "A  - Trapézio + Centroide":          ("trap", "centroid"),
    "B  - Triângulo + MOM":               ("tri",  "mom"),
    "A+B - Trapézio + MOM":               ("trap", "mom"),
}

if __name__ == "__main__":
    resultados, superficies = {}, {}
    for nome, (crit, df) in CONFIGS.items():
        sis, _ = construir_sistema(crit, df)
        minimo = avaliar(sis, 0, 0)
        maximo = avaliar(sis, 100, 10)
        xs, ys, Z = superficie(sis)
        # rugosidade: maior salto entre pontos vizinhos da malha
        salto = max(np.abs(np.diff(Z, axis=0)).max(), np.abs(np.diff(Z, axis=1)).max())
        # corte no meio da escala (Explorabilidade = 5): nº de níveis distintos
        corte = [avaliar(sis, x, 5) for x in np.linspace(0, 100, 101)]
        niveis = len(np.unique(np.round(corte, 2)))
        resultados[nome] = (minimo, maximo, salto, niveis)
        superficies[nome] = (xs, ys, Z)
        print(f"{nome:36s} | (0,0)={minimo:6.2f}% | (100,10)={maximo:6.2f}% "
              f"| maior salto={salto:5.2f} | níveis distintos (expl=5)={niveis}")

    # Figura obrigatória: superfície da abordagem recomendada
    xs, ys, Z = superficies["A0 - Triângulo + Centroide (base)"]
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    plot_superficie(ax, xs, ys, Z, "Superfície de Decisão 3D - Mamdani (Centroide)")
    plt.tight_layout()
    plt.savefig("superficie_decisao.png", dpi=150)
    plt.close()

    # Figura comparativa das 4 configurações
    fig = plt.figure(figsize=(14, 10))
    for k, (nome, (xs, ys, Z)) in enumerate(superficies.items(), 1):
        ax = fig.add_subplot(2, 2, k, projection="3d")
        plot_superficie(ax, xs, ys, Z, nome)
    plt.tight_layout()
    plt.savefig("comparativo_abordagens.png", dpi=130)
    plt.close()

    # Funções de pertinência da saída (triângulo x trapézio)
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
    for a, crit in zip(axs, ["tri", "trap"]):
        _, (_, _, u) = construir_sistema(crit, "centroid")
        for termo in u.terms:
            a.plot(u.universe, u[termo].mf, label=termo)
        a.set_title(f"Urgência - Crítica = {'trimf' if crit=='tri' else 'trapmf'}")
        a.set_xlabel("Urgência (%)"); a.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig("pertinencia_urgencia.png", dpi=130)
