# Resultados — Aula 10: Motor de Inferência Mamdani e Superfície 3D

**Disciplina:** Inteligência Computacional — Sprint 2 da AC-3
**Sistema:** Impacto (0–100 %) × Explorabilidade (0–10) → Urgência (0–100 %), 9 regras Mamdani, implementado com `scikit-fuzzy`.

---

## a) Desafio dos Extremos

### Resultados medidos (`lab01_aula10.py`)

| Configuração | Saída em (0, 0) | Saída em (100, 10) | Maior salto entre vizinhos da malha | Suavidade |
|---|---|---|---|---|
| Triângulo + **Centroide** (base) | 11,67 % | 90,00 % | 19,9 pts | Suave |
| **Abordagem A**: Trapézio (Crítica) + Centroide | 11,67 % | 89,17 % | 19,9 pts | Suave |
| **Abordagem B**: Triângulo + **MOM** | 0,00 % | 100,00 % | 58,0 pts | Degraus abruptos |
| A + B: Trapézio + MOM | 0,00 % | 95,00 % | 58,0 pts | Degraus abruptos |

> **Nota sobre os valores do enunciado (4,33 % e 87,5 %).** Esses números dependem dos parâmetros dos conjuntos de saída, que o enunciado não fornece. Com os conjuntos que adotei (Baixa [0,0,35]; Crítica [70,100,100]) o fenômeno é o mesmo, mas os números diferem (11,67 % e 90 %). O mecanismo explicado abaixo vale para qualquer escolha.

### Questão 1 — Por que o Centroide com triângulos não atinge 0 % nem 100 %?

Em (0, 0) só dispara uma regra (Impacto Baixo ∧ Explorabilidade Baixa → Urgência Baixa), com grau 1. A saída agregada é então o triângulo inteiro de "Urgência Baixa", e o Centroide devolve **o centro de massa dessa área**, não o ponto onde a pertinência é máxima.

Para um triângulo com vértices [0, 0, 35], o centro de massa é (0 + 0 + 35)/3 = **11,67**. Para a Crítica [70, 100, 100], é (70 + 100 + 100)/3 = **90**.

Como o triângulo se estende para dentro da escala, sua massa fica sempre deslocada para o interior. O Centroide só valeria 0 ou 100 se toda a massa estivesse concentrada exatamente na borda (um *singleton*). Isso é uma propriedade matemática do método (efeito de "média"), e não um bug do código.

### Questão 2 — O que muda ao usar Trapézio (`trapmf`) na borda superior da Crítica?

Resultado medido: **a saída em (100, 10) não sobe para 100 %. Ela cai de 90,00 % para 89,17 %.**

O trapézio [70, 90, 100, 100] cria um platô entre 90 e 100, o que acrescenta massa na região 90–100. Mas o trapézio também é "mais gordo" do que o triângulo na parte intermediária (de 70 a 90 ele sobe mais rápido), então o centro de massa ainda fica abaixo de 100, e levemente abaixo do valor do triângulo. A intuição de que "o trapézio crava 100 %" **não se confirma com o Centroide**. A suavidade no meio da escala é preservada (o maior salto é igual ao da base), porém o problema dos extremos continua.

O trapézio só aproximaria 100 % se o platô fosse bem estreito e colado na borda (por exemplo, [95, 99, 100, 100]). Mesmo assim, o Centroide nunca chegaria a 100 exatamente, e o formato do conjunto perderia o sentido semântico de "urgência crítica" gradual.

### Questão 3 — O que muda com a defuzzificação MOM (Mean of Maximum)?

O MOM calcula a média dos pontos onde a pertinência agregada é máxima. Com triângulos, o pico é um único ponto (0 ou 100), então o resultado é **exatamente 0 % e 100 %** nos extremos. O custo está no meio da escala: a saída passa a depender apenas da regra dominante, e o resultado vira **degraus**. O maior salto entre pontos vizinhos da malha subiu de **19,9 para 58,0 pontos**, e a superfície ganha "paredes" verticais (ver `comparativo_abordagens.png`). Combinar trapézio com MOM é pior: o platô 90–100 faz o MOM devolver 95 %, e portanto nem os extremos são cravados.

### Qual abordagem é mais recomendável?

| Critério | Centroide (tri ou trap) | MOM |
|---|---|---|
| Crava 0 % e 100 % nos extremos | Não | **Sim (só com triângulos)** |
| Suavidade no meio da escala | **Sim** | Não (degraus de até 58 pts) |
| Adequado para priorização contínua de incidentes | **Sim** | Não |

**Recomendação:** manter o **Centroide**. Para um sistema de priorização, uma superfície contínua importa mais do que atingir exatamente 0 % ou 100 %: duas ocorrências quase iguais não podem receber urgências muito diferentes. Se o requisito de extremos exatos for obrigatório, as alternativas que preservam a suavidade são:

1. **Normalizar a saída** linearmente, mapeando o mínimo e o máximo alcançáveis (11,67 e 90) para 0 e 100.
2. **Usar saída tipo Sugeno** (singletons em 0, 40, 70 e 100), que atinge os extremos e continua contínuo.

Nenhuma das duas abordagens do enunciado (A ou B) satisfaz sozinha os dois requisitos ao mesmo tempo. O trapézio com Centroide é suave, mas não crava; o MOM crava, mas perde a suavidade.

---

## b) Matriz de Regras 3×3 codificada

| Impacto \ Explorabilidade | Baixa (0–4) | Moderada (2–8) | Alta (6–10) |
|---|---|---|---|
| **Baixo (0–40)** | R1: Urgência Baixa | R2: Urgência Baixa | R3: Urgência Média |
| **Médio (20–80)** | R4: Urgência Média | R5: Urgência Alta | R6: Urgência Alta |
| **Alto (60–100)** | R7: Urgência Crítica | R8: Urgência Crítica | R9: Urgência Crítica |

Todas as 9 combinações estão cobertas (sem lacunas). Como os conjuntos de entrada se sobrepõem (Baixo/Médio entre 20 e 40; Médio/Alto entre 60 e 80; análogo para Explorabilidade), sempre ao menos uma regra dispara para qualquer par de entradas.

Parâmetros dos conjuntos de saída adotados: Baixa [0, 0, 35], Média [15, 40, 65], Alta [45, 70, 95], Crítica [70, 100, 100].

---

## c) Análise interpretativa da Superfície de Decisão 3D

Figura: `superficie_decisao.png` (Centroide, triângulos); comparação das quatro configurações em `comparativo_abordagens.png`.

- **Continuidade:** a superfície não tem saltos bruscos. As funções de pertinência se sobrepõem e o Centroide interpola entre as regras, então pequenas variações nas entradas geram pequenas variações na urgência.
- **Monotonia:** a urgência cresce (ou se mantém) tanto com o Impacto quanto com a Explorabilidade, coerente com a matriz de regras.
- **O Impacto domina:** a maior inclinação ocorre ao longo do eixo do Impacto. Para Impacto alto (acima de ~80), a superfície vira um **platô** em torno de 90 %, porque as três regras do grupo "Alto" resultam em Crítica independentemente da Explorabilidade.
- **A Explorabilidade modula nas faixas baixa e média:** com Impacto Baixo ela eleva a urgência de Baixa para Média (R3). Com Impacto Médio, de Média para Alta (R4 → R5/R6). Isso aparece como a rampa lateral da superfície.
- **Patamares e limites:** os "terraços" refletem os quatro níveis de saída (Baixa, Média, Alta, Crítica). A superfície varia de ≈ 11,7 % a ≈ 90 %, sem tocar 0 % e 100 %. Isso é o efeito do Centroide discutido na Questão 1.

---

## Artefatos

- `lab01_aula10.py` — código completo (9 regras, experimento e gráficos)
- `superficie_decisao.png` — superfície 3D
- `comparativo_abordagens.png` — as 4 configurações lado a lado
- `pertinencia_urgencia.png` — funções de pertinência da saída (trimf × trapmf)
