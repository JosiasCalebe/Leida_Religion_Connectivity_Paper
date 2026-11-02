# 03 - Seleção e pareamento de participantes

## Estratégia

1. **Amostra completa**: todos os 881 participantes com fMRI.
2. **Subamostra pareada (case-control)**: cada religioso (`religious_now == yes`, n = 187)
   recebe um não religioso com o mesmo sexo, lateralidade e nível educacional, escolhendo o
   candidato com menor distância `|Δidade| + |ΔSES|`. Resultado: 374 participantes.
3. **Pareamento estendido** (variante mais conservadora): mesmo pareamento exato, mas a
   distância é a média de `|Δ|` em idade, SES, `IST_fluid`, `IST_intelligence_total`, `BIS`,
   `NEO_A` e `NEO_C`. Resultado: 374 participantes.
4. **Criação religiosa entre não religiosos**: mesmo procedimento entre não religiosos
   criados em ambiente religioso x não religioso -> 141 x 141 = 282.

Os mesmos pareamentos foram feitos para sexo, escolaridade e criação religiosa (pastas
`*Filtered` em `06_`):

| Variável | Âncora | Pareado exatamente por | Critério de proximidade | N |
|---|---|---|---|---|
| Religião | religiosos | sexo, lateralidade, escolaridade | menor `\|Δidade\| + \|ΔSES\|` | 187 + 187 = 374 |
| Religião, estendido | religiosos | sexo, lateralidade, escolaridade | menor média de `\|Δ\|` em 7 variáveis (idade, SES, IST_fluid, IST total, BIS, NEO_A, NEO_C) | 187 + 187 = 374 |
| Gênero | homens | religião atual, lateralidade, escolaridade | menor `\|Δidade\| + \|ΔSES\|` | 380 + 380 = 760 |
| Criação religiosa | criados em ambiente religioso | sexo, lateralidade, escolaridade, religião atual | menor `\|Δidade\| + \|ΔSES\|` | 167 + 167 = 334 |
| Escolaridade | high (trios high-low-medium) | sexo, lateralidade, religião atual | par (low, medium) que minimiza `d(h,l) + d(h,m) + d(l,m)` | 85 x 3 = 255 |
| Criação religiosa (só não religiosos) | criados em ambiente religioso | sexo, lateralidade, escolaridade | menor `\|Δidade\| + \|ΔSES\|` | 141 + 141 = 282 |

Todos os pareamentos são gulosos e sem reposição: as âncoras são percorridas na ordem da
planilha de participantes e cada candidato escolhido sai do conjunto disponível.

## Scripts (`scripts/`)

| Script | O que faz |
|---|---|
| `SelectingParticipants_Religious_vs_NonReligious.ipynb` | Pareamento religioso x não religioso -> `selected_participantsReligious.xlsx` |
| `SelectingParticipants_NonReligious_Upbringing.ipynb` | Pareamento entre não religiosos com x sem criação religiosa -> `selected_participants-RU-RN-N.xlsx` |
| `SelectingParticipants_Gender.ipynb` | Pareamento homens x mulheres -> `selected_participantsGender.xlsx` |
| `SelectingParticipants_Education.ipynb` | Pareamento em trios high-low-medium -> `selected_participantsEducation.xlsx` (com `pair_id` e `original_index`) |
| `SelectingParticipants_ReligiousUpbringing.ipynb` | Pareamento criação religiosa yes x no (religiosos e não religiosos) -> `selected_participantsReligiousUpbringing.xlsx` |
| `SelectingParticipants_Religious_vs_NonReligious_Extended.ipynb` | Pareamento estendido religioso x não religioso (distância com medidas cognitivas e de personalidade) -> `selected_participantsOtherVariables09-15.xlsx` |
| `create_metadata_from_selection.py` | Gera `metadata.csv` (`subject_id,condition`) a partir de uma planilha de selecionados, excluindo `no_func_ids.csv`; a coluna-condição é escolhida no mapeamento |
| `select_participants_filter.py` | Extrai `participant_id,religious_upbringing` de `nao_religiosos.xlsx` |
| `filter_metadata_remove_medium.py` | Remove `medium` do metadata de escolaridade (comparação high x low) |
| `delete_timeseries_by_metadata.py` | Apaga de `time_series/` os sujeitos ausentes no `metadata.csv` (monta a entrada do PyLEiDA para uma subamostra). Tem `DRY_RUN` |

Os seis notebooks `SelectingParticipants_*` têm o mesmo formato: leem a planilha de
participantes (`PARTICIPANTS_CSV`), removem os 47 sujeitos sem func (928 -> 881), fazem o
pareamento e testam o balanço entre os grupos.
No topo de cada um, defina `DATA_ROOT` (pasta local com `ID1000Files/`) e, se quiser,
`OUTPUT_DIR`. Todos foram executados e reproduzem exatamente sujeitos, ordem e valores das
planilhas em `selected_participants/`.

Nas subamostras de religião (374) e de criação religiosa entre não religiosos (282), idade, SES
e as variáveis de pareamento ficam balanceadas, mas a inteligência (`IST_intelligence_total`)
ainda difere entre os grupos (p = 0,018 e p = 0,048). O pareamento estendido equilibra também a
inteligência (p = 0,97) e as demais variáveis da distância (todas com p > 0,15).

## Planilhas (`selected_participants/`)

| Arquivo | Conteúdo |
|---|---|
| `selected_participantsReligious.xlsx` | Pareamento religioso x não religioso (374) |
| `selected_participantsOtherVariables09-15.xlsx` | Pareamento estendido religioso x não religioso (374), com distância em 7 variáveis |
| `selected_participants-RU-RN-N.xlsx` | Não religiosos pareados por criação religiosa (282) |
| `selected_participantsGender.xlsx` | Pareamento por sexo (760) |
| `selected_participantsEducation.xlsx` | Pareamento por escolaridade (255) |
| `selected_participantsReligiousUpbringing.xlsx` | Pareamento por criação religiosa (334) |
| `nao_religiosos.xlsx` | Todos os não religiosos (694) com `religious_upbringing` |
| `religious_now_no.csv` | Ids dos não religiosos |

## Metadados por variável (`metadata/`)

Formato exigido pelo PyLEiDA: `subject_id,condition` (ids sequenciais, ver `01_`).

| Arquivo | Condição | N |
|---|---|---|
| `participants_religion.csv` | `religious` / `nonreligious` | 881 |
| `participants_gender.csv` | `female` / `male` | 881 |
| `participants_education.csv` | `high` / `medium` / `low` | 881 |
| `participants_religious_upbringing.csv` | `yes` / `no` | 881 |
| `participants_handedness.csv` | `right` / `left` | 881 |
| `participants_non_religious_upbringing.csv` | `yes` / `no` (só não religiosos) | 694 |
| `participants_education_last_generated.csv` | último `metadata.csv` gerado por `create_metadata_from_selection.py` (subamostra pareada de escolaridade, `high`/`medium`/`low`) | 255 |

Os `metadata.csv` das subamostras pareadas estão dentro de cada pasta de análise em
`06_LEiDA_Results/files_per_atlas/<atlas>/Filtered/<variável>/`.
