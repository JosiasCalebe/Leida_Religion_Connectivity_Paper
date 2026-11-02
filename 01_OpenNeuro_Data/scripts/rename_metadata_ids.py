"""
Arquivo original: import csv.py

Propósito: utilitário para substituir a primeira coluna de um CSV de metadados
por ids sequenciais no formato sub-0001 ... sub-0376 (limitado a 376 linhas).
Entrada : CSV exportado da planilha de participantes.
Saída   : <nome>_renamed.csv
"""

import csv
import os

def rename_first_column(input_file, output_file=None):
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_renamed{ext}"
    
    with open(input_file, 'r', newline='') as infile, \
         open(output_file, 'w', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read and write header row unchanged
        header = next(reader)
        writer.writerow(header)
        
        # Process remaining rows
        for idx, row in enumerate(reader, start=1):
            if idx > 376:
                break
            # Format new first column value with leading zeros
            new_value = f"sub-{idx:04d}"
            row[0] = new_value
            writer.writerow(row)
    
    print(f"File processed successfully. Output saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_filename = r"metadate.csv"  # Change this to your input file name
    rename_first_column(input_filename)