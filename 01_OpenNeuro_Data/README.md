# 01 - Dados do OpenNeuro (ID1000 / AOMIC)

## Origem dos dados

* Dataset: **AOMIC ID1000**, OpenNeuro **ds003097** (https://openneuro.org/datasets/ds003097).
  Snoek et al. (2021), *Scientific Data* 8:85.
* 928 participantes, 881 com fMRI funcional. Tarefa: assistir a um clipe de 11 min
  (*Koyaanisqatsi*), `task-moviewatching`, TR = 2,2 s, 3 mm isotrópico.
* Metadados demográficos (idade, sexo, escolaridade, lateralidade, `religious_now`,
  `religious_upbringing`, SES, inteligência, personalidade) vêm do `participants.tsv`
  do dataset e foram consolidados numa planilha Google (usada em `03_Participants_Selection`).

## Como baixar

```bash
# opção 1: openneuro-cli
npm install -g @openneuro/cli
openneuro download ds003097 ds003097/

# opção 2: DataLad
datalad install https://github.com/OpenNeuroDatasets/ds003097.git
```

Baixe `sub-*/anat`, `sub-*/func` (BOLD `task-moviewatching`) e, em
`derivatives/fmriprep/sub-*/func/`, os arquivos `*desc-confounds_regressors.tsv`
(usados em `04_Motion_Artifacts` para DVARS e framewise displacement).

## Estrutura local usada no projeto (não incluída aqui, ~88 GB)

```
ID1000Files/
  raw/
    in_use/sub-XXXX/{anat,func}/   <- sujeitos com dados funcionais
    no_func/sub-XXXX/              <- sujeitos sem func (excluídos)
    no_func_ids.csv
    metadata_*.csv                 <- condição por sujeito (ver 03_)
  anat_all/ func_all/              <- arquivos planos renomeados sub-0001_...
Derivatives/derivatives/fmriprep/sub-XXXX/func/*confounds_regressors.tsv
```

## Renumeração dos sujeitos

Os ids originais do ID1000 não são contínuos. Para o CONN os sujeitos foram renumerados
sequencialmente (`sub-0001` ... `sub-0881`). A correspondência está em:

* `id_mapping/id_mapping.csv` - `new_id,old_id` para todos os sujeitos com func.
* `id_mapping/id_mapping_religious.csv` - idem, para a subamostra pareada de religião (374).
* `id_mapping/no_func_ids.csv` - sujeitos sem dados funcionais.

**Atenção:** nos arquivos de `02_` a `06_` o `subject_id` é o **id novo** (sequencial).
Use `id_mapping.csv` para voltar ao id do OpenNeuro.

## Scripts (`scripts/`)

| Script | O que faz |
|---|---|
| `organize_subject_folders.py` | Renumera `sub-XXXX`, gera `id_mapping.csv`, copia func/anat para pastas planas, move sujeitos sem func para `no_func/` |
| `check_missing_func.py` | Lista sujeitos BIDS com `anat/` mas sem `func/` |
| `check_missing_func_flat.py` | Mesma checagem sobre as pastas planas `anat_all2/` e `func_all2/` |
| `list_no_func_ids.py` | Gera `no_func_ids.csv` |
| `rename_metadata_ids.py` | Troca a 1ª coluna de um CSV de metadados por ids sequenciais `sub-0001..` |
| `rename_roi_subject_numbers.py` | Unifica a numeração dos exports do CONN feitos em lotes (001-200, 201-400, 401-507) |
| `rename_rp_files.py` | Remove o prefixo duplicado `sub-XXXX_` dos arquivos de parâmetros de realinhamento |
| `rename_roi_to_old_id.py` | Converte `ROI_SubjectNNN.mat` do id novo para o id original via `id_mapping.csv` |

Os caminhos no topo de cada script são relativos à pasta local de dados do projeto (ver
README raiz); cada um tem um cabeçalho descrevendo entradas e saídas.
