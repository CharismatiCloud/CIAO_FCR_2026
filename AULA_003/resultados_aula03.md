# LAB-01 - Compreensão e Execução

==================================================
ALGORITMO GENÉTICO PASSO A PASSO
==================================================

População inicial: [[0, 1, 0, 1, 0], [1, 1, 1, 0, 0], [0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 1, 1, 0, 1], [1, 0, 1, 1, 0]]

==================== GERAÇÃO 0 ====================

Avaliação dos indivíduos:
  [0, 1, 0, 1, 0] → x=10 → f(x)=100
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [0, 1, 0, 1, 0] → x=10 → f(x)=100
  [0, 1, 1, 0, 1] → x=13 → f(x)=169
  [1, 0, 1, 1, 0] → x=22 → f(x)=484

 Melhor: x = 28 → f(x) = 784

==================== GERAÇÃO 1 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [1, 1, 1, 0, 1] → x=29 → f(x)=841

 Melhor: x = 29 → f(x) = 841

==================== GERAÇÃO 2 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 0, 0, 0] → x=24 → f(x)=576
  [1, 1, 1, 0, 1] → x=29 → f(x)=841

 Melhor: x = 29 → f(x) = 841

==================== GERAÇÃO 3 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 0, 0, 0] → x=24 → f(x)=576

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 4 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 0, 0, 0] → x= 8 → f(x)= 64
  [0, 1, 1, 1, 1] → x=15 → f(x)=225

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 5 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 6 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 0, 1, 1, 1] → x=23 → f(x)=529
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 0, 1] → x=29 → f(x)=841
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 0, 1] → x=25 → f(x)=625

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 7 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 0, 1, 0, 1] → x=21 → f(x)=441
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [1, 1, 1, 1, 1] → x=31 → f(x)=961

 Melhor: x = 31 → f(x) = 961

==================================================
RESULTADO FINAL
==================================================

Melhor indivíduo: [1, 1, 1, 1, 1]
x = 31
f(x) = 961

Ótimo global: x = 31, f(x) = 961
Erro: 0

Basicamente entendemos o que cada uma das variaveis funcionam, os bits são os valores possiveis para x que elevará ao quadrado para chegar ao resultado

# LAB-02 - Execução código pronto
original:
==================================================
ONEMAX - AG com 30 indivíduos, 50 gerações
==================================================
Geração   0: Melhor = 15/20, Média = 10.63
Geração  10: Melhor = 20/20, Média = 18.53
Geração  20: Melhor = 20/20, Média = 19.63
Geração  30: Melhor = 20/20, Média = 19.60
Geração  40: Melhor = 20/20, Média = 19.70

 MELHOR FITNESS: 20/20
   Ótimo = 20 (todos os bits são 1)


Novo:
==================================================
ONEMAX - AG com 30 indivíduos, 50 gerações
==================================================
Geração   0: Melhor = 13/20, Média = 10.20
Geração  10: Melhor = 20/20, Média = 19.63
Geração  20: Melhor = 20/20, Média = 19.33
Geração  30: Melhor = 20/20, Média = 19.70
Geração  40: Melhor = 20/20, Média = 19.70

 MELHOR FITNESS: 20/20
   Ótimo = 20 (todos os bits são 1)


==================================================
DESAFIO: Mude os parâmetros e veja o que acontece!
==================================================
1. Aumente a TAXA_MUT para 0.1. O que acontece?
2. Diminua POPULACAO para 10. O que acontece?
3. Aumente GERACOES para 100. O que acontece?
4. Mude ELITE para 0. O que acontece?

Respostas:
1. fica com o melhor mais proximo do otimo
2. o melhor e média demoram mais para chegar no ótimo
3. melhor e média ficam mais proximo do otimo
4. ele não preserva nenhum da população

# lab03_aula03_CIAO

Anterior:
============================================================
ALGORITMO GENÉTICO
Otimização de f(x) = x * sin(3x)
============================================================
Geração   0: Melhor f(x) = 8.7280 (x = 8.9804)
Geração  10: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  20: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  30: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  40: Melhor f(x) = 8.9019 (x = 8.9020)

Novo:
============================================================
ALGORITMO GENÉTICO
Otimização de f(x) = x * sin(3x)
============================================================
Geração   0: Melhor f(x) = 8.8769 (x = 8.9412)
Geração  10: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  20: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  30: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  40: Melhor f(x) = 8.9019 (x = 8.9020)

obs: não altera muito dependendo das configurações
