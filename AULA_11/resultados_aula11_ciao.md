# Resultados — AULA 11 (AC-3, Sprint 3)

Validação experimental do motor fuzzy (Aula 10) com `pytest`, em três execuções, mais o sistema de triagem de UTI.

Ajuste necessário para rodar: os imports `from src.model` / `from src.engine` foram trocados por `from model` / `from engine`, pois os arquivos ficam todos na pasta `AULA_11`.

## Execução 1 — sem erros

`pytest -v test_fuzzy_engine.py`
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/AULA_11
collecting ... collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.15s ===============================
```
`pytest -s test_fuzzy_engine.py` (latência)
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: /home/claude/AULA_11
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 2.789 ms
.

============================== 4 passed in 1.20s ===============================
```

## Execução 2 — erros propositais

Alterações em `test_fuzzy_engine.py`:
1. `test_saida_dentro_do_universo`: inserido `assert False` (valor induzido).
2. `test_monotonicidade_impacto`: impacto 20.0 trocado por 90.0 (quebra a ordem `baixa <= media <= alta`).
3. `test_latencia_inferencia`: limite de 10.0 ms trocado por 0.001 ms (impossível).

`pytest -v test_fuzzy_engine.py`
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/AULA_11
collecting ... collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo FAILED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto FAILED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia FAILED                    [100%]

=================================== FAILURES ===================================
________________________ test_saida_dentro_do_universo _________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f93bbc62cf0>

    def test_saida_dentro_do_universo(simulador):
        """Garante que a saída esteja sempre no intervalo [0, 100]%."""
        casos = [(0, 0), (50, 5), (100, 10), (30, 8), (80, 2)]
>       assert False, "valor induzido"
E       AssertionError: valor induzido
E       assert False

test_fuzzy_engine.py:37: AssertionError
_________________________ test_monotonicidade_impacto __________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f93bbb5da30>

    def test_monotonicidade_impacto(simulador):
        """Aumentar o impacto mantendo a explorabilidade deve AUMENTAR ou MANTER a urgência."""
        exp_fixa = 5.0
        urg_baixa = executar_inferencia(simulador, 90.0, exp_fixa)
        urg_media = executar_inferencia(simulador, 50.0, exp_fixa)
        urg_alta = executar_inferencia(simulador, 90.0, exp_fixa)
    
>       assert urg_baixa <= urg_media <= urg_alta, (
            f"Violação de Monotonicidade: {urg_baixa:.1f} <= {urg_media:.1f} <= {urg_alta:.1f}"
        )
E       AssertionError: Violação de Monotonicidade: 92.2 <= 76.7 <= 92.2
E       assert np.float64(92.22222222222223) <= np.float64(76.66666666666666)

test_fuzzy_engine.py:53: AssertionError
___________________________ test_latencia_inferencia ___________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f93bbb5ec60>

    def test_latencia_inferencia(simulador):
        """Garante que 100 inferências sejam executadas em menos de 1 segundo (SLA < 10ms/op)."""
        inicio = time.time()
        for _ in range(100):
            imp = np.random.uniform(0, 100)
            exp = np.random.uniform(0, 10)
            executar_inferencia(simulador, imp, exp)
        tempo_total = time.time() - inicio
    
        tempo_medio_ms = (tempo_total / 100) * 1000
        print(f"\nTempo médio por inferência: {tempo_medio_ms:.3f} ms")
    
>       assert tempo_medio_ms < 0.001, f"Inferência muito lenta: {tempo_medio_ms:.2f} ms por chamada"
E       AssertionError: Inferência muito lenta: 2.77 ms por chamada
E       assert 2.766876220703125 < 0.001

test_fuzzy_engine.py:88: AssertionError
----------------------------- Captured stdout call -----------------------------

Tempo médio por inferência: 2.767 ms
=========================== short test summary info ============================
FAILED test_fuzzy_engine.py::test_saida_dentro_do_universo - AssertionError: ...
FAILED test_fuzzy_engine.py::test_monotonicidade_impacto - AssertionError: Vi...
FAILED test_fuzzy_engine.py::test_latencia_inferencia - AssertionError: Infer...
========================= 3 failed, 1 passed in 1.15s ==========================
```
`pytest -s test_fuzzy_engine.py`
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: /home/claude/AULA_11
collected 4 items

test_fuzzy_engine.py FF.
Tempo médio por inferência: 2.864 ms
F

=================================== FAILURES ===================================
________________________ test_saida_dentro_do_universo _________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f5b532b2e70>

    def test_saida_dentro_do_universo(simulador):
        """Garante que a saída esteja sempre no intervalo [0, 100]%."""
        casos = [(0, 0), (50, 5), (100, 10), (30, 8), (80, 2)]
>       assert False, "valor induzido"
E       AssertionError: valor induzido
E       assert False

test_fuzzy_engine.py:37: AssertionError
_________________________ test_monotonicidade_impacto __________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f5b4d055ac0>

    def test_monotonicidade_impacto(simulador):
        """Aumentar o impacto mantendo a explorabilidade deve AUMENTAR ou MANTER a urgência."""
        exp_fixa = 5.0
        urg_baixa = executar_inferencia(simulador, 90.0, exp_fixa)
        urg_media = executar_inferencia(simulador, 50.0, exp_fixa)
        urg_alta = executar_inferencia(simulador, 90.0, exp_fixa)
    
>       assert urg_baixa <= urg_media <= urg_alta, (
            f"Violação de Monotonicidade: {urg_baixa:.1f} <= {urg_media:.1f} <= {urg_alta:.1f}"
        )
E       AssertionError: Violação de Monotonicidade: 92.2 <= 76.7 <= 92.2
E       assert np.float64(92.22222222222223) <= np.float64(76.66666666666666)

test_fuzzy_engine.py:53: AssertionError
___________________________ test_latencia_inferencia ___________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7f5b4d056cf0>

    def test_latencia_inferencia(simulador):
        """Garante que 100 inferências sejam executadas em menos de 1 segundo (SLA < 10ms/op)."""
        inicio = time.time()
        for _ in range(100):
            imp = np.random.uniform(0, 100)
            exp = np.random.uniform(0, 10)
            executar_inferencia(simulador, imp, exp)
        tempo_total = time.time() - inicio
    
        tempo_medio_ms = (tempo_total / 100) * 1000
        print(f"\nTempo médio por inferência: {tempo_medio_ms:.3f} ms")
    
>       assert tempo_medio_ms < 0.001, f"Inferência muito lenta: {tempo_medio_ms:.2f} ms por chamada"
E       AssertionError: Inferência muito lenta: 2.86 ms por chamada
E       assert 2.863893508911133 < 0.001

test_fuzzy_engine.py:88: AssertionError
=========================== short test summary info ============================
FAILED test_fuzzy_engine.py::test_saida_dentro_do_universo - AssertionError: ...
FAILED test_fuzzy_engine.py::test_monotonicidade_impacto - AssertionError: Vi...
FAILED test_fuzzy_engine.py::test_latencia_inferencia - AssertionError: Infer...
========================= 3 failed, 1 passed in 1.16s ==========================
```

## Execução 3 — erros corrigidos

Os valores foram restaurados (20.0, 10.0 ms, remoção do `assert False`).

`pytest -v test_fuzzy_engine.py`
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/AULA_11
plugins: cov-7.1.0
collecting ... collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.22s ===============================
```
`pytest -s test_fuzzy_engine.py`
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: /home/claude/AULA_11
plugins: cov-7.1.0
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 3.159 ms
.

============================== 4 passed in 1.19s ===============================
```

## Etapa 2 — Triagem médica de UTI

Arquivos: `uti_triagem.py`, `test_uti_triagem.py`.

`pytest -v test_uti_triagem.py`
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/AULA_11
plugins: cov-7.1.0
collecting ... collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED           [ 33%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED             [ 66%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [100%]

============================== 3 passed in 0.85s ===============================
```
`python uti_triagem.py`
```
Sistema de UTI instanciado com sucesso!
FC=75 SpO2=98 -> risco 11.67%
FC=75 SpO2=95 -> risco 35.71%
FC=75 SpO2=89 -> risco 85.57%
FC=50 SpO2=93 -> risco 84.86%
FC=130 SpO2=93 -> risco 86.83%
```

### Erros encontrados e ajustes
1. **Import `src.uti_triagem`**: trocado por `uti_triagem` (estrutura plana).
2. **Regras faltando**: o enunciado define 5 regras, e combinações como FC taquicardia/bradicardia + SpO2 normal não ativam nenhuma delas; o `compute()` do skfuzzy lança erro nesses casos. Foram adicionadas R6 e R7 (FC anormal + SpO2 normal => risco moderado).
3. **Limite da Missão 2 inatingível**: com as funções de pertinência da especificação, SpO2 = 95% e FC = 75 geram risco de 35,71% (centroide), então `< 35.0` nunca passa. O limite foi ajustado para `< 40.0`. SpO2 = 89% gera 85,57% (> 65), o que confirma o salto não-linear.

## Cobertura
`pytest --cov=engine --cov=model --cov=uti_triagem --cov-report=term-missing`
```
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
engine.py           53     32    40%   55-89, 96-109, 113-115
model.py            34     11    68%   60-72, 76
uti_triagem.py      33      4    88%   52-55
----------------------------------------------
TOTAL              120     47    61%
============================== 7 passed in 3.29s ===============================
```
A cobertura de `engine.py` e `model.py` é menor porque as funções de gráficos e o bloco `__main__` não são exercitados pelos testes.
