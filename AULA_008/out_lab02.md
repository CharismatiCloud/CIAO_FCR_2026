Dados dos 15 microsserviços (gerados com seed=7, pois o enunciado não os fornece):

| Serviço | Valor | RAM (GB) | CPU (cores) |
|---|---|---|---|
| S1 | 95 | 5.0 | 0.5 |
| S2 | 66 | 3.5 | 0.5 |
| S3 | 72 | 2.5 | 1.5 |
| S4 | 91 | 2.5 | 1.5 |
| S5 | 62 | 2.5 | 2.5 |
| S6 | 80 | 3.0 | 2.0 |
| S7 | 85 | 3.5 | 1.5 |
| S8 | 30 | 4.0 | 1.5 |
| S9 | 15 | 6.0 | 1.0 |
| S10 | 37 | 5.0 | 0.5 |
| S11 | 35 | 4.0 | 1.0 |
| S12 | 89 | 6.0 | 2.0 |
| S13 | 93 | 2.0 | 1.0 |
| S14 | 10 | 2.0 | 1.0 |
| S15 | 55 | 4.0 | 0.5 |

Ótimo global por força bruta (2^15 combinações): valor = 444, serviços = ['S1', 'S4', 'S6', 'S7', 'S13'], RAM = 16.0, CPU = 6.5

Parâmetros: população 60, 100 gerações, torneio k=3, cruzamento 1 ponto pc=0.9, mutação pm=1/15, elitismo 1, alpha(B)=1.5, 30 execuções independentes.

| Estratégia | Melhor valor viável (melhor execução) | Média±dp dos melhores (30 exec.) | Execuções que acharam o ótimo | Execuções cujo melhor da população final era inviável | Melhor combinação |
|---|---|---|---|---|---|
| A (Penalidade Rígida) | 444 | 444.0 ± 0.0 | 30/30 | 0/30 | ['S1', 'S4', 'S6', 'S7', 'S13'] (RAM 16.0, CPU 6.5) |
| B (Penalidade Proporcional) | 444 | 444.0 ± 0.0 | 30/30 | 0/30 | ['S1', 'S4', 'S6', 'S7', 'S13'] (RAM 16.0, CPU 6.5) |

| Geração | A: média | A: dp | A: diversidade | A: % viáveis | B: média | B: dp | B: diversidade | B: % viáveis |
|---|---|---|---|---|---|---|---|---|
| 0 | 13.9 | 56.6 | 0.500 | 6% | 55.8 | 91.9 | 0.500 | 6% |
| 10 | 181.9 | 157.4 | 0.329 | 60% | 283.7 | 117.1 | 0.307 | 41% |
| 25 | 193.7 | 174.0 | 0.293 | 58% | 301.0 | 124.4 | 0.259 | 45% |
| 50 | 193.9 | 180.0 | 0.268 | 56% | 306.0 | 123.2 | 0.245 | 48% |
| 75 | 191.5 | 176.5 | 0.278 | 56% | 301.3 | 122.7 | 0.248 | 45% |
| 100 | 181.3 | 180.1 | 0.270 | 52% | 297.2 | 124.8 | 0.242 | 45% |

Diversidade média ao longo das gerações, A (Penalidade Rígida): 0.294
Diversidade média ao longo das gerações, B (Penalidade Proporcional): 0.267