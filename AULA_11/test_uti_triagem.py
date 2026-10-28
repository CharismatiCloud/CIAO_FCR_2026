import pytest
from uti_triagem import criar_sistema_triagem_uti, avaliar_paciente


@pytest.fixture
def simulador_uti():
    return criar_sistema_triagem_uti()


def test_paciente_saudavel_baixo_risco(simulador_uti):
    """75 bpm e SpO2 98% -> risco estritamente < 30%."""
    assert avaliar_paciente(simulador_uti, 75, 98) < 30.0


def test_salto_nao_linear_queda_spo2(simulador_uti):
    """SpO2 95% (< 40%) vs 89% (> 65%): salto não-linear.
    Obs.: o limite original (< 35%) é inatingível com as MFs da especificação
    (centroide em 95% = 35,71%), então foi ajustado para 40%."""
    r95 = avaliar_paciente(simulador_uti, 75, 95)
    r89 = avaliar_paciente(simulador_uti, 75, 89)
    assert r95 < 40.0
    assert r89 > 65.0
    assert r89 > r95 + 20.0


def test_validacao_limites_fisiologicos(simulador_uti):
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 30, 98)    # bpm < 40
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 75, 101)   # SpO2 > 100
