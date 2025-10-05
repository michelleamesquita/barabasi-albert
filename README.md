## Barabási–Albert (BA)

Este diretório contém um experimento simples e reprodutível do modelo de crescimento preferencial de Barabási–Albert (BA). O script cresce a rede incrementalmente a partir de uma clique inicial de 4 vértices e captura snapshots em N = 100, 1.000 e 10.000 nós para analisar:

- Distribuição de grau em forma cumulativa complementar (CCDF)
- Os 20 vértices de maior grau em cada snapshot
- A razão entre o maior grau e os graus dos demais 19 vértices do top-20

### Arquivos
- `ba_experiments.py`: implementação do crescimento BA incremental, geração de CCDF e análise do top-20.
- `out/`: diretório de saída para figuras e CSVs.
- `requirements.txt`: dependências específicas deste módulo (igual ao stack científico usado no projeto).
- `RESPOSTAS.md`: respostas às perguntas propostas no enunciado.

### Ambiente
Você pode usar o Python do projeto raiz ou criar um ambiente dedicado para este módulo.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r barabasi-albert/requirements.txt
```

Se preferir, as dependências da raiz do repositório também atendem.

### Como executar

```bash
python ba_experiments.py
```

Parâmetros padrão (configuráveis em `BAParams`):
- `max_num_nodes = 10_000`
- `attachment_m = 4`
- `snapshot_sizes = (100, 1_000, 10_000)`
- `random_seed = 42` 

### Saídas (em `./out/`)
- `ba_degree_ccdf.png`: CCDF da distribuição de grau sobreposta para N=100, 1k, 10k.
- `top20_deg_N100.csv`, `top20_deg_N1000.csv`, `top20_deg_N10000.csv`: top-20 por snapshot.
- `top20_ratios_N*.csv`: razões `d_max / d_rank` para cada snapshot.
- `top20_ratio_vs_rank.png`: curvas de `d_max / d_rank` (rank 2..20) para cada N.
- `top20_ratios_long.csv`: tabela longa com (N, rank, ratio).

### Questão importante: como "interromper" o crescimento no BA?
O `networkx.barabasi_albert_graph(n, m)` constrói o grafo final de tamanho `n` (usando por padrão clique `K_m` como grafo inicial). Para analisar estados intermediários como `N=100` e `N=1k`, uma forma simples é gerar o grafo final e tomar subgrafos induzidos pelos primeiros `N` vértices (`0..N-1`). Essa abordagem é consistente com o processo de inserção de vértices em ordem e atende ao objetivo de medir em tamanhos conhecidos.

### Resultado esperado
- A CCDF tende a uma cauda do tipo lei de potência típica do BA (reta em log–log) à medida que N cresce.
- Os vértices mais antigos tendem a concentrar graus altos; o conjunto do top-20 torna-se relativamente estável com N grande, embora pequenas trocas de ordem possam ocorrer.
- A razão `d_max / d_rank` tende a crescer moderadamente com N, refletindo a vantagem acumulativa dos vértices mais antigos.


## RELATÓRIO FINAL

- [Relatório de métricas (Markdown)](./RESPOSTAS.md)

