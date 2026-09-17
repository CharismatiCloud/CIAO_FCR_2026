[LAB 01] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70

 ## Respostas Das Questões Técnicas

 ### 1\. Como o uso da busca local 2-opt afeta o equilíbrio entre Exploration e Exploitation na busca de caminhos?
 A busca local 2-opt aumenta a **exploitation (exploração das boas soluções já encontradas)**. Depois que cada formiga constrói uma rota usando os feromônios e a informação heurística das distâncias, o 2-opt tenta melhorar essa rota localmente, invertendo trechos do caminho e verificando se isso reduz o custo total.

 Dessa forma, o ACO continua responsável pela **exploration**, pois as formigas podem construir diferentes caminhos de maneira probabilística. Já o 2-opt intensifica a busca nas regiões promissoras do espaço de soluções, procurando aperfeiçoar as rotas encontradas.

 Portanto, o algoritmo híbrido combina os dois comportamentos: o ACO favorece a diversificação e o 2-opt favorece a intensificação. O benefício é encontrar soluções melhores mais rapidamente, embora uma busca local muito dominante possa reduzir a diversidade das soluções e aumentar a tendência de convergência para ótimos locais.

 ### 2\. O que aconteceria com a convergência do algoritmo se a taxa de evaporação (`rho`) fosse definida em `0.0` (sem evaporação)?

 não reduziria os valores de feromônio. Assim, todo feromônio depositado pelas formigas permaneceria acumulado durante as iterações.

 Consequentemente, os caminhos que receberem bastante feromônio passariam a ter uma influência cada vez maior sobre a escolha das próximas rotas. Isso aumenta a **exploitation** e pode fazer o algoritmo convergir rapidamente para determinadas soluções.

 Por outro lado, a ausência de evaporação reduz a capacidade de esquecer informações antigas. Um caminho que tenha recebido muito feromônio nas primeiras iterações pode continuar influenciando fortemente as decisões posteriores, mesmo que existam caminhos melhores.

 Assim, com `rho = 0.0`, é esperado que a diversidade da busca diminua e que aumente o risco de **convergência prematura para um ótimo local**. A evaporação é importante no ACO justamente para equilibrar a influência das experiências anteriores e manter a possibilidade de explorar novas soluções.

[LAB 02]

Geração 1: Melhor fitness = 12
Geração 2: Melhor fitness = 14
Geração 3: Melhor fitness = 15
Geração 4: Melhor fitness = 15
Geração 5: Melhor fitness = 14
Geração 6: Melhor fitness = 15
Geração 7: Melhor fitness = 15
Geração 8: Melhor fitness = 15
Geração 9: Melhor fitness = 15
Geração 10: Melhor fitness = 15

[LAB 02] Resultado final
Melhor indivíduo: [0 1 1 1 1]
Peso total: 8
Valor total: 15
Fitness: 15

## Questão 1

A mutação é responsável por introduzir diversidade genética na população. Ela altera aleatoriamente alguns genes dos indivíduos, evitando que a população fique presa muito cedo em uma solução que não seja a melhor possível.

Se a taxa de mutação for configurada em 100%, todos os genes serão invertidos em todas as gerações. Isso fará com que todos os bits dos indivíduos sejam alterados, causando uma mudança muito grande na população e podendo dificultar a convergência do algoritmo para uma boa solução.

## Questão 2

A penalização do fitness é fundamental porque impede que soluções que ultrapassem a capacidade máxima sejam consideradas boas pelo algoritmo.

Quando o peso total é maior que `max_weight`, o fitness recebe valor 0. Dessa forma, soluções inválidas têm pouca ou nenhuma chance de serem selecionadas para reprodução.

Isso faz com que, ao longo das gerações, o algoritmo favoreça indivíduos que respeitam a restrição de peso enquanto procuram maximizar o valor dos ativos.

# LAB 03 - PSO: Inércia, Componente Cognitiva e Social

**Tema:** Otimização Contínua de Parâmetros e Limiares.

## Equação implementada

A linha desbalanceada foi completada com a equação clássica de atualização de velocidade do PSO:

```python
V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))
```

Onde:
- `w * V[i]` é o termo de **inércia** (mantém a direção/velocidade anterior);
- `c1 * r1 * (pbest_X[i] - X[i])` é o termo **cognitivo** (atrai a partícula de volta à sua própria melhor posição já encontrada);
- `c2 * r2 * (gbest_X - X[i])` é o termo **social** (atrai a partícula em direção à melhor posição encontrada por todo o enxame).

## Output da execução

```
[LAB 03] Melhor posição encontrada pelo Enxame (gbest): [-0.01309447 -0.02659493]
[LAB 03] Fitness da melhor posição (gbest): 0.0008787551443636512
```

(Executado com `np.random.seed(42)` para reprodutibilidade. O algoritmo convergiu, como esperado, para próximo do mínimo global da função esférica em (0, 0).)

## Respostas das Questões Técnicas

### 1 - O que acontece com o comportamento das partículas se zerarmos a componente cognitiva (c1 = 0)?

Ao zerar `c1`, o termo `c1 * r1 * (pbest_X[i] - X[i])` desaparece da equação de velocidade, ou seja, a partícula deixa de ser atraída pela sua própria melhor posição individual (pbest). Ela passa a se mover apenas com base na inércia (velocidade anterior) e na componente social (atração pelo gbest, a melhor posição global do enxame).

Na prática, isso faz com que:
- Todas as partículas convirjam de forma mais rápida e homogênea em direção ao gbest, já que não há mais um "puxão" individual concorrente;
- O enxame perde diversidade de busca mais cedo, aumentando o risco de **convergência prematura** para um mínimo local (caso a função de fitness tenha múltiplos mínimos), pois as partículas deixam de explorar regiões próprias e passam a seguir quase que exclusivamente o líder do grupo;
- O algoritmo se aproxima de um comportamento mais "gregário"/social puro, sacrificando a capacidade de exploração individual em favor da exploração coletiva (explotação em torno do gbest).

### 2 - Qual a função do parâmetro de Inércia (w) na busca por mínimos globais?

O parâmetro de inércia `w` controla o quanto da velocidade da iteração anterior é preservado na atualização da velocidade atual. Ele regula o equilíbrio entre **exploração (exploration)** e **explotação/refinamento (exploitation)**:

- **Valores altos de w** (próximos de 1 ou maiores) fazem a partícula manter grande parte do seu movimento anterior, favorecendo a exploração do espaço de busca — útil no início da otimização para varrer regiões distantes e evitar ficar presa prematuramente em mínimos locais;
- **Valores baixos de w** (próximos de 0) reduzem a influência da velocidade anterior, fazendo a partícula responder mais fortemente aos termos cognitivo e social, favorecendo a explotação — refinar a busca em torno das melhores posições já encontradas (pbest/gbest), útil nas fases finais para convergir com precisão;
- É comum usar um `w` que decai ao longo das iterações (começando alto e diminuindo), combinando boa exploração inicial com refinamento posterior, o que ajuda o algoritmo a convergir para o mínimo global sem ficar preso a mínimos locais nem oscilar indefinidamente.

No código deste laboratório, `w = 0.5` é um valor fixo intermediário, equilibrando moderadamente inércia e resposta ao pbest/gbest ao longo de todas as 15 iterações.

LAB 04 - ACO: Feromônio, Evaporação e Atratividade

Tema: Otimização de Caminhos e Grafos de Rede.

Observação: o enunciado original trazia duas perguntas coladas no item "2" (sem separação de texto). Elas foram desmembradas abaixo nas questões 2 e 3 para que ambas fossem respondidas integralmente.

Trechos implementados
python
# TODO 1: Evaporação em toda a matriz de feromônio
pheromone_matrix = (1 - rho) * pheromone_matrix

# TODO 2: Depósito de feromônio em cada aresta percorrida, inversamente proporcional ao custo do caminho
for path, cost in zip(paths, costs):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        pheromone_matrix[u][v] += 1.0 / cost

Também foi incluído o cálculo da atratividade inicial (eta), definida como o inverso da latência de cada enlace (eta = 1 / latência), para responder à questão 3.

Output da execução
[LAB 04] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]

[LAB 04] Matriz de Atratividade Inicial (eta = 1/latência):
 [[0.         0.2        0.5        0.11111111]
 [0.2        0.         0.33333333 1.        ]
 [0.5        0.33333333 0.         0.14285714]
 [0.11111111 1.         0.14285714 0.        ]]
Respostas das Questões Técnicas
1 - Por que a evaporação do feromônio é necessária no algoritmo ACO?

A evaporação (representada pelo fator (1 - rho) aplicado a toda a matriz de feromônio) reduz gradualmente a intensidade do feromônio depositado em todas as arestas do grafo ao longo das iterações. Ela é necessária porque:

Evita que o algoritmo fique preso permanentemente em caminhos encontrados nas primeiras iterações, mesmo que eles não sejam os melhores — sem evaporação, o feromônio depositado só cresce, "engessando" a preferência do enxame por rotas subótimas descobertas cedo;
Introduz um mecanismo de "esquecimento" que dá espaço para que caminhos melhores, descobertos mais tarde, possam competir e se tornar dominantes;
Ajuda a manter o equilíbrio entre exploração (busca de novas rotas) e explotação (reforço das rotas já boas), algo essencial para a convergência do algoritmo para o ótimo global (ou uma boa aproximação dele).
2 - O que ocorreria em grafos complexos sem ela?

Sem evaporação, em grafos mais complexos (com muitos nós e arestas, e múltiplos caminhos possíveis) o algoritmo tenderia a:

Sofrer convergência prematura/estagnação: as primeiras arestas que recebem depósito de feromônio acumulam vantagem permanente, e como o feromônio nunca decai, essa vantagem só aumenta a cada iteração, tornando extremamente improvável que as formigas explorem novas rotas alternativas;
Ficar preso em mínimos locais, já que o algoritmo perde a capacidade de "corrigir o rumo" quando encontra, mais tarde, um caminho de menor custo total do que aquele que foi reforçado inicialmente;
Apresentar falta de diversidade nas soluções exploradas pelo enxame, reduzindo a qualidade geral da otimização à medida que o grafo cresce em tamanho e número de caminhos possíveis, pois o espaço de busca não é varrido de forma adequada.
3 - Qual a relação matemática entre a latência de um enlace e sua atratividade inicial (eta) para as formigas?

A atratividade inicial de um enlace, comumente chamada de eta (η), é definida como o inverso da latência (custo) daquele enlace:

eta(u, v) = 1 / latência(u, v)

Ou seja, a relação é inversamente proporcional: quanto menor a latência entre dois roteadores, maior a atratividade heurística daquele enlace, tornando-o mais provável de ser escolhido por uma formiga na regra de decisão probabilística do ACO (que combina eta com a intensidade do feromônio, tipicamente na forma feromônio^α * eta^β). Enlaces com alta latência (custo alto) recebem, portanto, atratividade inicial baixa, desestimulando — mas não impedindo — seu uso pelas formigas.

[Lab05]
# LAB 05 — MEMÉTICO: Meta-heurística + Busca Local

[LAB 05] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
[LAB 05] Solução Refinada: [ 2.5 -3.1] | Fitness: 37.7698

## Questão 1

A diferença fundamental é que o Algoritmo Genético Puro utiliza principalmente operadores evolutivos, como seleção, crossover e mutação, para explorar o espaço de soluções.

Já o Algoritmo Memético combina esses operadores com uma busca local. Depois de gerar uma solução, o algoritmo tenta melhorá-la individualmente por meio de pequenas alterações. Dessa forma, o Algoritmo Memético realiza tanto exploração do espaço de busca quanto intensificação das soluções encontradas.

## Questão 2

Executar a busca local sobre todos os indivíduos a cada geração aumenta significativamente o custo computacional.

Isso acontece porque, além das operações normais do algoritmo evolutivo, cada indivíduo precisa realizar várias avaliações de vizinhança. Por exemplo, com uma população de 100 indivíduos, 50 gerações e 20 passos de busca local por indivíduo, podem ser necessárias até 100.000 avaliações adicionais da função objetivo.

O benefício é que as soluções podem ser refinadas mais rapidamente, mas o tempo de execução e o número de avaliações aumentam proporcionalmente.
