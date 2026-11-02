"""
Arquivo original: ArquivosNew/GordonEducation/LEiDA_results/filter_metadata.py

Propósito: remove as linhas com condition == "medium" do metadata.csv de escolaridade,
deixando apenas high x low (comparação reportada no paper).
ATENÇÃO: sobrescreve o arquivo de entrada.
"""

import pandas as pd

# Read the CSV file
df = pd.read_csv('./ArquivosNew/GordonEducation/LEiDA_results/metadata.csv')

# Filter out rows where condition is 'medium'
df_filtered = df[df['condition'] != 'medium']

# Write the filtered data back to the same file
df_filtered.to_csv('./ArquivosNew/GordonEducation/LEiDA_results/metadata.csv', index=False)

print("Successfully removed all 'medium' conditions from metadata.csv. Only 'high' and 'low' remain.")