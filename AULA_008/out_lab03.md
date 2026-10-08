Matriz de latências D (10x10, gerada a partir de coordenadas com seed=11, pois o enunciado não a fornece):

```
[[   0.0   66.7   42.9   37.4   82.9   24.1   57.9   28.9   54.2   69.0]
 [  66.7    0.0  100.7   54.1   68.7   53.6   25.4   89.0   48.9   56.3]
 [  42.9  100.7    0.0   80.2   85.7   47.2   83.2   14.1   66.8   76.9]
 [  37.4   54.1   80.2    0.0  100.6   48.5   61.0   66.2   71.2   85.6]
 [  82.9   68.7   85.7  100.6    0.0   59.0   44.9   82.7   29.9   15.0]
 [  24.1   53.6   47.2   48.5   59.0    0.0   37.7   36.0   30.1   44.9]
 [  57.9   25.4   83.2   61.0   44.9   37.7    0.0   73.4   23.7   31.4]
 [  28.9   89.0   14.1   66.2   82.7   36.0   73.4    0.0   60.0   72.0]
 [  54.2   48.9   66.8   71.2   29.9   30.1   23.7   60.0    0.0   15.1]
 [  69.0   56.3   76.9   85.6   15.0   44.9   31.4   72.0   15.1    0.0]]
```

Parâmetros: rho=0.2, alpha=1.0, beta=3.0, 30 formigas, 100 iterações, deposita as 3 melhores, Q=100.0, 20 execuções.

Matriz de Adjacência final (ACO, evaporação só nas melhores topologias):

```
[[0 0 0 1 0 1 0 1 0 0]
 [0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [1 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1]
 [1 0 0 0 0 0 0 0 1 0]
 [0 1 0 0 0 0 0 0 1 0]
 [1 0 1 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 1 0 0 1]
 [0 0 0 0 1 0 0 0 1 0]]
```

Arestas: [(0, 3), (0, 5), (0, 7), (1, 6), (2, 7), (4, 9), (5, 8), (6, 8), (8, 9)], nº de arestas = 9, árvore válida = True

| Método | Latência total |
|---|---|
| MST (Prim, ótimo exato) | 213.8 |
| ACO evaporação só nas melhores (enunciado): melhor / média±dp | 213.8 / 213.8 ± 0.0 (ótimo em 20/20 execuções) |
| ACO evaporação global (clássico): melhor / média±dp | 213.8 / 213.8 ± 0.0 (ótimo em 20/20 execuções) |
| Topologia aleatória única (seed 2024) | 570.5 |
| Topologias aleatórias (2000): média±dp / melhor | 502.2 ± 61.0 / 300.9 |

| Comparação | Ganho de redução de latência |
|---|---|
| ACO (melhor) vs topologia aleatória única | 62.52% |
| ACO (melhor) vs média de 2000 aleatórias | 57.43% |
| ACO (média das 20 exec.) vs média de 2000 aleatórias | 57.43% |
| ACO global (média) vs média aleatórias | 57.43% |
| Gap do ACO (melhor) para o MST | 0.00% |