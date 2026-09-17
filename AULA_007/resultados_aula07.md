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
