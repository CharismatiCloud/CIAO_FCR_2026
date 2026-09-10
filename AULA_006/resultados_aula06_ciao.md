lab01_aula06_ciao

1. Por que o ACO utiliza várias formigas em vez de apenas uma formiga procurando a melhor rota?

O ACO utiliza várias formigas para explorar diferentes caminhos da rede. Cada formiga pode encontrar uma rota diferente, aumentando a diversidade da busca. Dessa forma, o algoritmo não fica limitado a uma única tentativa e tem maior possibilidade de encontrar uma solução de baixo custo.

2. Por que uma rota de menor custo recebe mais feromônio?

Uma rota de menor custo recebe mais feromônio porque é considerada uma solução melhor. Como as próximas formigas utilizam o feromônio como uma das informações para escolher seus caminhos, elas passam a ter maior probabilidade de seguir as rotas que apresentaram bons resultados anteriormente.

Assim, ocorre um processo de reforço: rotas melhores recebem mais feromônio e, consequentemente, tornam-se mais atrativas para as próximas formigas.

3. O que poderia acontecer se não existisse evaporação do feromônio?

Sem a evaporação, o feromônio das primeiras experiências permaneceria na rede indefinidamente. Isso poderia fazer com que as formigas continuassem seguindo caminhos que foram escolhidos anteriormente, mesmo que posteriormente fossem encontradas rotas melhores.

Consequentemente, o algoritmo poderia ficar preso em uma solução não ideal e perder a capacidade de explorar novas possibilidades. A evaporação é importante porque reduz gradualmente a influência das experiências antigas e permite que novas soluções também sejam consideradas.

lab02_aula06_ciao

Iteração 01 | Melhor custo: 23.11
Iteração 02 | Melhor custo: 23.11
Iteração 03 | Melhor custo: 23.11
Iteração 04 | Melhor custo: 23.11
Iteração 05 | Melhor custo: 23.11
Iteração 06 | Melhor custo: 23.11
Iteração 07 | Melhor custo: 23.11
Iteração 08 | Melhor custo: 23.11
Iteração 09 | Melhor custo: 23.11
Iteração 10 | Melhor custo: 23.11
Iteração 11 | Melhor custo: 23.11
Iteração 12 | Melhor custo: 23.11
Iteração 13 | Melhor custo: 23.11
Iteração 14 | Melhor custo: 23.11
Iteração 15 | Melhor custo: 23.11
Iteração 16 | Melhor custo: 23.11
Iteração 17 | Melhor custo: 23.11
Iteração 18 | Melhor custo: 23.11
Iteração 19 | Melhor custo: 23.11
Iteração 20 | Melhor custo: 23.11
Iteração 21 | Melhor custo: 23.11
Iteração 22 | Melhor custo: 23.11
Iteração 23 | Melhor custo: 23.11
Iteração 24 | Melhor custo: 23.11
Iteração 25 | Melhor custo: 23.11
Iteração 26 | Melhor custo: 23.11
Iteração 27 | Melhor custo: 23.11
Iteração 28 | Melhor custo: 23.11
Iteração 29 | Melhor custo: 23.11
Iteração 30 | Melhor custo: 23.11
Iteração 31 | Melhor custo: 23.11
Iteração 32 | Melhor custo: 23.11
Iteração 33 | Melhor custo: 23.11
Iteração 34 | Melhor custo: 23.11
Iteração 35 | Melhor custo: 23.11
Iteração 36 | Melhor custo: 23.11
Iteração 37 | Melhor custo: 23.11
Iteração 38 | Melhor custo: 23.11
Iteração 39 | Melhor custo: 23.11
Iteração 40 | Melhor custo: 23.11
Iteração 41 | Melhor custo: 23.11
Iteração 42 | Melhor custo: 23.11
Iteração 43 | Melhor custo: 23.11
Iteração 44 | Melhor custo: 23.11
Iteração 45 | Melhor custo: 23.11
Iteração 46 | Melhor custo: 23.11
Iteração 47 | Melhor custo: 23.11
Iteração 48 | Melhor custo: 23.11
Iteração 49 | Melhor custo: 23.11
Iteração 50 | Melhor custo: 23.11

========== RESULTADO DO EXPERIMENTO ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 1.0
BETA: 2.0
Taxa de evaporação: 0.5
Q: 100
Melhor rota: D -> E -> C -> A -> B -> F -> D
Melhor custo: 23.11


========== FEROMÔNIO FINAL ==========
A -> B: 173.1081
A -> C: 173.1082
A -> D: 0.0002
A -> E: 0.0000
A -> F: 0.0002
B -> A: 173.1081
B -> C: 0.0002
B -> D: 0.0000
B -> E: 0.0027
B -> F: 173.1057
C -> A: 173.1082
C -> B: 0.0002
C -> D: 0.0000
C -> E: 173.1058
C -> F: 0.0025
D -> A: 0.0002
D -> B: 0.0000
D -> C: 0.0000
D -> E: 173.1081
D -> F: 173.1083
E -> A: 0.0000
E -> B: 0.0027
E -> C: 173.1058
E -> D: 173.1081
E -> F: 0.0000
F -> A: 0.0002
F -> B: 173.1057
F -> C: 0.0025
F -> D: 173.1083
F -> E: 0.0000

## Respostas

 **1\. Quando aumentamos o ALPHA, a influência da experiência acumulada pelas formigas aumenta ou diminui?**

 A influência da experiência acumulada **aumenta**. Valores maiores de ALPHA fazem com que o feromônio tenha mais peso na escolha dos caminhos.

 **2\. O que acontece quando o BETA é baixo ou alto?**

 - **BETA baixo:** o custo/distância influencia menos a escolha das formigas.
- **BETA alto:** caminhos de menor custo ficam mais atrativos, pois a informação heurística recebe maior peso.

 **3\. O que acontece quando o algoritmo esquece rapidamente as experiências anteriores?**

 Com uma taxa de evaporação alta, o feromônio desaparece mais rapidamente. Assim, as experiências antigas têm menos influência e o algoritmo tende a **explorar novas rotas**, mas pode ter mais dificuldade para manter uma boa solução encontrada anteriormente.

 **4\. O que acontece quando aumentamos o número de formigas de 5 para 50?**

 Com mais formigas, o algoritmo explora **mais rotas a cada iteração**, aumentando a possibilidade de encontrar uma boa solução. Porém, isso também aumenta o custo computacional do algoritmo.

lab03_aula06_ciao

Questões para serem respondidas:

1 - Por que a fórmula da atratividade utiliza 1 / custo
em vez de utilizar diretamente o custo?
R: Porque quanto menor o custo, maior deve ser a atratividade.
Usando 1/custo, caminhos mais baratos recebem maior atratividade.

2 - O que acontece com a atratividade quando uma rota
recebe mais feromônio?
R: A atratividade aumenta, pois o feromônio influencia
positivamente a escolha do caminho.

3 - Por que a função construir_rota() precisa impedir
que a formiga visite novamente um nó que já está na rota?
R: Para evitar ciclos e visitas desnecessárias aos mesmos nós,
permitindo que a formiga construa uma rota válida até o destino.

Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0

lab04_aula06_ciao

1 - Como o feromônio ajuda o ACO a aprender quais caminhos são melhores?

O feromônio é depositado nas arestas utilizadas pelas formigas. Rotas com menor custo recebem uma quantidade maior de feromônio. Com o passar das iterações, as formigas ficam mais propensas a escolher caminhos que possuem mais feromônio, fazendo o algoritmo aprender quais caminhos apresentam melhores resultados.

2 - Diferença entre explorar e aproveitar caminhos

Explorar significa experimentar caminhos diferentes para descobrir novas possibilidades. Aproveitar significa continuar escolhendo caminhos que já apresentaram bons resultados. O ACO precisa equilibrar os dois: explorar para não ficar preso em uma solução ruim e aproveitar para melhorar soluções que já se mostraram boas.

3 - Como melhorar o desempenho em uma rede muito maior?

Eu investigaria primeiro a quantidade de formigas e o número de iterações, pois eles determinam diretamente quantas rotas serão calculadas. Em uma rede muito grande, testar muitas formigas durante muitas iterações pode aumentar bastante o tempo de execução. Também seria interessante otimizar a construção das rotas e limitar a busca a vizinhos promissores.


========== RESULTADO ==========

Melhor rota encontrada:
[0, 1, 2, 4, 5]

Melhor custo:
8.0

\n1 - Como o feromônio ajuda o ACO a aprender quais caminhos são melhores?\n\nO feromônio é depositado nas arestas utilizadas pelas formigas. Rotas com menor custo recebem uma quantidade maior de feromônio. Com o passar das iterações, as formigas ficam mais propensas a escolher caminhos que possuem mais feromônio, fazendo o algoritmo aprender quais caminhos apresentam melhores resultados.\n\n2 - Diferença entre explorar e aproveitar caminhos\n\nExplorar significa experimentar caminhos diferentes para descobrir novas possibilidades. Aproveitar significa continuar escolhendo caminhos que já apresentaram bons resultados. O ACO precisa equilibrar os dois: explorar para não ficar preso em uma solução ruim e aproveitar para melhorar soluções que já se mostraram boas.\n\n3 - Como melhorar o desempenho em uma rede muito maior?\n\nEu investigaria primeiro a quantidade de formigas e o número de iterações, pois eles determinam diretamente quantas rotas serão calculadas. Em uma rede muito grande, <img width="691" height="470" alt="download" src="https://github.com/user-attachments/assets/e9b95cbe-513e-4ada-8d6a-adfed1e4149f" />
