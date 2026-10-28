import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl


def criar_sistema_triagem_uti():
    """Cria o motor fuzzy (Mamdani) de triagem clínica de UTI."""
    fc = ctrl.Antecedent(np.arange(40, 161, 1), 'freq_cardiaca')
    spo2 = ctrl.Antecedent(np.arange(70, 101, 1), 'spo2')
    risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')
    risco.defuzzify_method = 'centroid'

    fc['bradicardia'] = fuzzy.trimf(fc.universe, [40, 40, 60])
    fc['normal'] = fuzzy.trimf(fc.universe, [50, 75, 100])
    fc['taquicardia'] = fuzzy.trapmf(fc.universe, [90, 110, 160, 160])

    spo2['critica'] = fuzzy.trapmf(spo2.universe, [70, 70, 88, 91])
    spo2['limitrofe'] = fuzzy.trimf(spo2.universe, [89, 93, 96])
    spo2['normal'] = fuzzy.trapmf(spo2.universe, [94, 97, 100, 100])

    risco['baixo'] = fuzzy.trimf(risco.universe, [0, 0, 35])
    risco['moderado'] = fuzzy.trimf(risco.universe, [25, 50, 75])
    risco['critico'] = fuzzy.trapmf(risco.universe, [65, 85, 100, 100])

    regras = [
        ctrl.Rule(spo2['critica'], risco['critico']),                                # R1
        ctrl.Rule(fc['bradicardia'] & spo2['limitrofe'], risco['critico']),          # R2
        ctrl.Rule(fc['taquicardia'] & spo2['limitrofe'], risco['critico']),          # R3
        ctrl.Rule(fc['normal'] & spo2['limitrofe'], risco['moderado']),              # R4
        ctrl.Rule(fc['normal'] & spo2['normal'], risco['baixo']),                    # R5
        # Regras complementares (cobertura): sem elas, FC anormal + SpO2 normal
        # não ativa nenhuma regra e o skfuzzy lança erro no compute().
        ctrl.Rule(fc['bradicardia'] & spo2['normal'], risco['moderado']),            # R6
        ctrl.Rule(fc['taquicardia'] & spo2['normal'], risco['moderado']),            # R7
    ]
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(regras))


def avaliar_paciente(simulador, bpm, spo2_val):
    """Valida entradas fisiológicas, executa a inferência e retorna o risco (%)."""
    if not (40 <= bpm <= 160):
        raise ValueError(f"bpm fora de [40, 160]: {bpm}")
    if not (70 <= spo2_val <= 100):
        raise ValueError(f"SpO2 fora de [70, 100]: {spo2_val}")
    simulador.input['freq_cardiaca'] = bpm
    simulador.input['spo2'] = spo2_val
    simulador.compute()
    return simulador.output['risco']


if __name__ == "__main__":
    sim = criar_sistema_triagem_uti()
    print("Sistema de UTI instanciado com sucesso!")
    for bpm, s in [(75, 98), (75, 95), (75, 89), (50, 93), (130, 93)]:
        print(f"FC={bpm} SpO2={s} -> risco {avaliar_paciente(sim, bpm, s):.2f}%")
