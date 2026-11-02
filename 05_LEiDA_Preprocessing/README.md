# 05 - Entrada e execução do PyLEiDA

## Instalação

```bash
conda create --name pL python=3.9
conda activate pL
pip install pyleida
```

(`numpy >= 2` removeu `np.float_`; os notebooks fazem `np.float_ = np.float64` logo após o
import para manter compatibilidade.)

## Formato de entrada

Uma pasta por análise com:

```
<analise>/
  metadata.csv              subject_id,condition   (ex.: sub-0001,religious)
  rois_labels.txt           um rótulo por linha, mesma ordem de tseries.csv
  rois_coordinates.csv      X,Y,Z
  time_series/
    sub-0001/tseries.csv    N_ROIs x N_volumes (333 x 290 Gordon; 360 x 290 Glasser)
    sub-0002/tseries.csv
    ...
```

`files_per_atlas/Gordon/` e `files_per_atlas/Glasser/` trazem `rois_labels.txt`,
`rois_coordinates.csv` e o `metadata.csv` da amostra completa (881, religião). As pastas
`time_series/` (~1,5 GB por atlas) **não** estão no repositório; gere-as com
`02_CONN_Exports/scripts/mat_to_pyleida_timeseries.R`.

Para montar uma subamostra: copie a pasta completa, troque `metadata.csv` pelo da subamostra
(ver `03_`) e rode `scripts/delete_timeseries_by_metadata.py`.

## Execução

`scripts/leida_pipeline_template.ipynb` (notebook-modelo, com explicações em português sobre
leading eigenvector, clustering e teste por permutação):

```python
from pyleida import Leida
import numpy as np; np.float_ = np.float64

ld = Leida('<caminho da pasta da análise>')
ld.fit_predict(TR=2.2, paired_tests=False, n_perm=5_000, save_results=True)
```

Isso cria `LEiDA_results/` com:

| Arquivo | Conteúdo |
|---|---|
| `eigenvectors.csv` | leading eigenvector de cada volume de cada sujeito (pesado, ~1,7 GB) |
| `clustering/models/model{K}.pkl` | modelos K-means, K = 2..20 |
| `clustering/predictions.csv` | estado atribuído a cada volume, por K |
| `clustering/clustering_performance.csv/png` | Dunn score etc. por K |
| `dynamics_metrics/k_{K}/occupancies.csv`, `dwell_times.csv`, `transitions_probabilities.csv` | métricas por sujeito |
| `dynamics_metrics/k_{K}/*_stats.csv` | teste t por permutação entre condições, com α de Bonferroni |
| `dynamics_metrics/*_pyramid.png`, `*_scatter_pvalues.png` | resumos gráficos |

Cada análise em `06_LEiDA_Results` contém o notebook efetivamente executado (`leida_run.ipynb`,
sem outputs) e seu HTML renderizado (`report_*.html`).
