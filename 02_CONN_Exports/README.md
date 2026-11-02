# 02 - Pré-processamento no CONN e exports

## Export das séries temporais

O CONN exporta, por sujeito, `ROI_SubjectNNN_SessionNNN.mat` contendo `names`, `data`
(série temporal de cada ROI, 290 volumes) e `xyz` (coordenadas). Os `.mat` (~1 GB, 1 122
arquivos) **não estão** no repositório; ficam em `Religion/ROIsData` e `Others/ROIs*`
na análise local.

### `scripts/mat_to_pyleida_timeseries.R`

Converte os `.mat` no formato do PyLEiDA:

```
<output_dir>/time_series/sub-0001/tseries.csv   (N_ROIs x N_volumes, sem cabeçalho)
<output_dir>/time_series/sub-0002/tseries.csv
...
```

Defina no topo `input_dir`, `output_dir` e `atlas <- "gordon"` ou `"glasser"`. A função
`basic_files()` gera `rois_labels_<atlas>.txt` e `rois_coordinates_<atlas>.csv`.

## Arquivos por atlas

| Pasta | Arquivos |
|---|---|
| `Gordon_Exports/` | `rois_labels.txt` (333, ex.: `L_Default_1`), `rois_labels_old.txt` (rótulos antes da renomeação), `rois_coordinates.csv` (X,Y,Z em MNI), `gordon333NodeNames.txt` |
| `Glasser_Exports/` | `rois_labels.txt` (360, ex.: `Right_V1`), `rois_coordinates.csv`, `glasser360NodeNames.txt` |
| `atlas/` | `gordon333MNI.nii.gz`, `glasser360MNI.nii.gz` - parcelações em MNI usadas em `plot_states_on_surf2` |

A ordem das linhas em `rois_labels.txt` e `rois_coordinates.csv` é a ordem das linhas de
`tseries.csv` e das colunas de `eigenvectors.csv`.
