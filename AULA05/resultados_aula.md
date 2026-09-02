# Resultados_aula.md — AC-2 Parte 1 — PSO

## Nota importante sobre uma correção feita no código

No enunciado da **Missão 3**, a função `fitness()` estava definida para retornar `-custo_total`,
mas o laço de otimização usa a lógica padrão de minimização (`if fitness < gBest_fit`), a mesma
usada nas Missões 1 e 2. Minimizar `-custo_total` equivale a **maximizar** `custo_total` — ou
seja, o algoritmo, como estava especificado, otimizaria o problema errado (o oposto do que se
pede no cenário: "minimizar o custo total de entrega").

Isso foi confirmado empiricamente: rodando a versão literal do enunciado, os 5 centros
convergiram para os cantos do mapa (ex.: (10,10), (10,0)) e o custo final (16955) ficou **pior**
que uma solução aleatória (6544) — o oposto do esperado.

Correção aplicada (nas Missões 3 e 4): `fitness()` passou a retornar `custo_total` diretamente
(positivo), mantendo a mesma comparação `if fitness < gBest_fit`. Com isso, o PSO minimiza o
custo corretamente, como confirmam os resultados abaixo (custo caiu de ~6540 para ~3515,
melhoria de 46%).

---

## Outputs das Missões

### Missão 1 — A Partícula Solitária

```
Posição inicial: 2.7885
Fitness inicial: 7.7759

Iteração  1: pos =  2.0286, fitness =   4.1150
Iteração  2: pos =  1.4206, fitness =   2.0180
Iteração  3: pos =  0.9342, fitness =   0.8727
Iteração  4: pos =  0.5451, fitness =   0.2971
Iteração  5: pos =  0.2338, fitness =   0.0547
Iteração  6: pos = -0.0153, fitness =   0.0002
Iteração  7: pos = -0.2145, fitness =   0.0460
Iteração  8: pos = -0.1319, fitness =   0.0174
Iteração  9: pos =  0.0769, fitness =   0.0059
Iteração 10: pos =  0.0360, fitness =   0.0013
Iteração 11: pos = -0.0348, fitness =   0.0012
Iteração 12: pos = -0.0535, fitness =   0.0029
Iteração 13: pos = -0.0576, fitness =   0.0033
Iteração 14: pos =  0.0313, fitness =   0.0010
Iteração 15: pos = -0.0049, fitness =   0.0000
Iteração 16: pos = -0.0339, fitness =   0.0011
Iteração 17: pos = -0.0166, fitness =   0.0003
Iteração 18: pos =  0.0226, fitness =   0.0005
Iteração 19: pos = -0.0054, fitness =   0.0000
Iteração 20: pos = -0.0273, fitness =   0.0007

RESULTADO FINAL
Posição final: -0.027285
Fitness final: 0.000744
Ótimo global: x = 0.000000, f(x) = 0.000000
Erro: 0.027285
```
<img width="1189" height="490" alt="image" src="https://github.com/user-attachments/assets/14b40972-734c-453d-81dc-dc6f8c2ddead" />

### Missão 2 — O Enxame (Rosenbrock)

```
Início: Melhor fitness = 3.363231
Iteração  10: Melhor = 0.213414
Iteração  20: Melhor = 0.182157
Iteração  30: Melhor = 0.000468
Iteração  40: Melhor = 0.000468
Iteração  50: Melhor = 0.000348

Fim: Melhor fitness = 0.000348
Ótimo global: f(1,1) = 0.000000
Melhor posição encontrada: [1.01106523, 1.02075228]
```
<img width="1362" height="490" alt="image" src="https://github.com/user-attachments/assets/73e07c50-3d37-4a2c-8ebd-6bf82cd2a371" />

### Missão 3 — Otimização Logística

```
DADOS DO PROBLEMA:
   - 50 clientes
   - 5 centros de distribuição
   - Demanda média: 51.0 unidades

OTIMIZANDO...
  Iteração  20: Custo = 3716.12
  Iteração  40: Custo = 3581.58
  Iteração  60: Custo = 3526.28
  Iteração  80: Custo = 3517.56
  Iteração 100: Custo = 3514.93

RESULTADO FINAL:
   Tempo de execução: 0.65 segundos
   Custo total (PSO): 3514.93
   Custo médio de soluções aleatórias (referência): 6540.80
   Melhoria: 46.3%
   Centros de distribuição:
      Centro 1: (2.70, 5.32)
      Centro 2: (0.59, 8.65)
      Centro 3: (5.47, 1.76)
      Centro 4: (0.90, 1.94)
      Centro 5: (7.74, 6.12)
```
<img width="1389" height="490" alt="image" src="https://github.com/user-attachments/assets/f4be2994-92bc-48cc-84f3-71a39274f470" />

### Missão 4 — Otimização de Parâmetros

| Experimento      | Custo Médio | Melhor Custo | Pior Custo |
|------------------|-------------|--------------|------------|
| Padrão           | 3638.88     | 3547.08      | 3712.66    |
| Inércia Alta     | 3951.15     | 3772.40      | 4145.73    |
| Inércia Baixa    | 3647.04     | 3514.29      | 3797.89    |
| Cognitivo Alto   | 3750.04     | 3671.45      | 3808.38    |
| Social Alto      | 3952.36     | 3890.59      | 4051.99    |
| Mais Partículas  | 3635.02     | 3523.28      | 3677.28    |

- **Melhor configuração:** Mais Partículas (60 partículas, w=0.7, c1=1.8, c2=1.8)
- **Pior configuração:** Social Alto (w=0.7, c1=1.8, c2=2.5)

<img width="1389" height="790" alt="image" src="https://github.com/user-attachments/assets/d2fcd193-7718-4e2a-8da7-6516f0174c2f" />

---

## RELATÓRIO FINAL PSO

### PARTE 1: O QUE VOCÊ APRENDEU?

**1. Explique com suas palavras o que é o PSO e como ele funciona.**

O PSO (Particle Swarm Optimization, ou Otimização por Enxame de Partículas) é um algoritmo
de otimização inspirado no comportamento coletivo de bandos de pássaros ou cardumes de peixes
procurando comida. Cada "partícula" representa uma solução candidata para o problema (no nosso
caso, um conjunto de coordenadas). As partículas se movem pelo espaço de busca guiadas por três
forças: (1) sua **inércia**, que mantém parte da direção do movimento anterior; (2) sua própria
melhor experiência (`pBest`), puxando a partícula de volta ao melhor lugar que ela mesma já
visitou; e (3) a melhor experiência do grupo (`gBest`), puxando-a em direção ao melhor lugar já
descoberto por qualquer partícula do enxame. A cada iteração, a velocidade de cada partícula é
recalculada combinando esses três fatores (com pesos `w`, `c1` e `c2`, mais um componente
aleatório para explorar o espaço), e a posição é atualizada somando a nova velocidade. Repetindo
esse processo por várias iterações, o enxame converge progressivamente para regiões de baixo
custo (ou alto benefício) da função objetivo, sem precisar calcular derivadas nem conhecer a
forma exata da função — por isso é tão útil em problemas contínuos, complexos e com muitas
variáveis, como o de localização de centros de distribuição.

**2. Qual a diferença entre pBest e gBest? Por que ambos são importantes?**

`pBest` (personal best) é a melhor posição que **uma partícula específica** já visitou durante
toda a busca — é a "memória individual" dela. `gBest` (global best) é a melhor posição
encontrada por **qualquer partícula do enxame inteiro** até o momento — é o "conhecimento
coletivo" compartilhado por todos. Os dois são importantes porque equilibram exploração e
explotação: se só existisse `pBest`, cada partícula buscaria isoladamente, sem trocar
informação, e o enxame demoraria muito mais para convergir (ou várias partículas ficariam presas
em regiões ruins). Se só existisse `gBest`, todas as partículas convergiriam rapidamente demais
para um único ponto, arriscando ficar presas em mínimos locais sem nunca explorar outras regiões
do espaço de busca. A combinação dos dois faz com que cada partícula equilibre "lembrar do que
funcionou bem para ela" com "seguir a informação de que o grupo encontrou algo melhor",
resultando em uma busca mais robusta e eficiente.

### PARTE 2: SUA EXPERIÊNCIA COM AS MISSÕES

**Missão 1 – A Partícula Solitária:**

A partícula encontrou o mínimo? **(X) Sim**, com erro final de apenas ~0.027 em relação ao
ótimo (x=0).

Quantas iterações foram necessárias? **~15–20** (o fitness já estava próximo de zero por volta
da iteração 6, mas continuou oscilando em torno do mínimo até o fim das 20 iterações
configuradas).

Dificuldade: **( ) Fácil (X) Médio ( ) Difícil** — a lógica é simples, mas exige atenção ao
transcrever corretamente a fórmula de atualização de velocidade.

**Missão 2 – O Enxame:**

O enxame encontrou o mínimo global? **(X) Sim**, convergindo para f ≈ 0.00035 na posição
(1.011, 1.021), muito próximo do ótimo teórico (1, 1).

Compare com a Missão 1: O enxame foi mais rápido? **(X) Sim** — mesmo em um problema mais
difícil (Rosenbrock é uma função "vale estreito", notoriamente difícil para otimizadores), o
enxame de 20 partículas convergiu de forma consistente, aproveitando a cooperação via `gBest`
para escapar de regiões ruins mais rápido do que uma única partícula conseguiria.

Dificuldade: **( ) Fácil (X) Médio ( ) Difícil** — trabalhar com arrays NumPy de 2 dimensões e
gerenciar o dicionário de cada partícula exige mais cuidado que a Missão 1.

**Missão 3 – Problema Corporativo:**

Compare com o custo inicial: Melhorou? **(X) Sim** — o custo caiu de ~6540 (média de soluções
aleatórias) para 3514.93 com o PSO, uma melhoria de **46.3%**.

Quantos centros foram alocados? **5**

Dificuldade: **( ) Fácil ( ) Médio (X) Difícil** — generalizar o PSO para 10 dimensões e, principalmente,
identificar e corrigir o problema de sinal na função de fitness (que fazia o algoritmo otimizar
na direção errada) foi o ponto mais desafiador da atividade.

**Missão 4 – Otimização de Parâmetros:**

Melhor configuração encontrada: **w=0.7, c1=1.8, c2=1.8, partículas=60** (custo médio 3635.02)

Pior configuração encontrada: **w=0.7, c1=1.8, c2=2.5, partículas=30** (custo médio 3952.36)

Dificuldade: **( ) Fácil (X) Médio ( ) Difícil** — o código do PSO em si já estava pronto; o
trabalho foi rodar, comparar e interpretar os experimentos.

**3. O que você observou sobre o efeito de:**

- **Inércia (w):** valores muito altos (w=0.9) pioraram o desempenho (custo médio 3951, o segundo
  pior resultado) — a partícula mantém velocidade alta demais e "passa direto" pelas boas
  regiões, dificultando o refinamento fino perto do ótimo. Um valor baixo (w=0.5) teve
  desempenho parecido com o padrão, sugerindo que reduzir um pouco a inércia ajuda a "frear" a
  busca perto da convergência sem prejudicar muito a exploração inicial.
- **Cognitivo (c1):** aumentar o peso da memória individual (c1=2.5) piorou levemente o
  resultado (custo médio 3750 vs. 3639 do padrão) — partículas mais "individualistas" exploram
  demais seus próprios pontos de referência e cooperam menos com o restante do enxame.
- **Social (c2):** aumentar o peso do conhecimento global (c2=2.5) foi o que mais piorou o
  resultado (custo médio 3952, o pior de todos) — com atração social excessiva, o enxame converge
  cedo demais para o `gBest` atual, perdendo diversidade e ficando mais suscetível a mínimos
  locais.
- **Número de partículas:** dobrar o número de partículas (30→60) trouxe a melhor melhoria
  observada (custo médio 3635, o menor de todos, com o menor desvio-padrão) — mais partículas
  cobrem melhor o espaço de busca e aumentam a chance de alguma delas começar perto de uma boa
  região, ao custo de mais processamento por iteração.

**4. Qual configuração você recomenda para este problema? Por quê?**

Recomendo a configuração **"Mais Partículas"** (w=0.7, c1=1.8, c2=1.8, 60 partículas), pois foi
a que obteve o menor custo médio (3635.02) e também o menor desvio-padrão entre execuções
(57.41), indicando resultados mais consistentes e confiáveis — importante em um problema real de
decisão logística, onde não se quer depender de "sorte" na inicialização aleatória. O custo
computacional extra de dobrar o número de partículas é pequeno frente ao ganho de qualidade e
estabilidade da solução, especialmente considerando que o problema tem apenas 10 dimensões e o
PSO já roda em menos de 1 segundo mesmo com mais partículas.
