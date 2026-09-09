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

lab04_aula06_ciao

1 - Como o feromônio ajuda o ACO a aprender quais caminhos são melhores?

O feromônio é depositado nas arestas utilizadas pelas formigas. Rotas com menor custo recebem uma quantidade maior de feromônio. Com o passar das iterações, as formigas ficam mais propensas a escolher caminhos que possuem mais feromônio, fazendo o algoritmo aprender quais caminhos apresentam melhores resultados.

2 - Diferença entre explorar e aproveitar caminhos

Explorar significa experimentar caminhos diferentes para descobrir novas possibilidades. Aproveitar significa continuar escolhendo caminhos que já apresentaram bons resultados. O ACO precisa equilibrar os dois: explorar para não ficar preso em uma solução ruim e aproveitar para melhorar soluções que já se mostraram boas.

3 - Como melhorar o desempenho em uma rede muito maior?

Eu investigaria primeiro a quantidade de formigas e o número de iterações, pois eles determinam diretamente quantas rotas serão calculadas. Em uma rede muito grande, testar muitas formigas durante muitas iterações pode aumentar bastante o tempo de execução. Também seria interessante otimizar a construção das rotas e limitar a busca a vizinhos promissores.
