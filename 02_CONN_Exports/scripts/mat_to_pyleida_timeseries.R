# Arquivo original: script_matToPyLeida.R
#
# Propósito: converte os exports de ROI do CONN toolbox (ROI_SubjectNNN_SessionNNN.mat,
# um por sujeito, contendo as séries temporais denoised de todos os atlas) no formato
# exigido pelo PyLEiDA: time_series/sub-XXXX/tseries.csv (N_ROIs x N_volumes).
#   - Seleciona apenas as ROIs do atlas desejado (prefixo atlasGordon / atlasGlasser).
#   - A função basic_files() (não chamada no loop) gera rois_labels_*.txt e
#     rois_coordinates_*.csv a partir do mesmo .mat.
# Entrada : pasta com os .mat exportados do CONN (ex.: Religion/ROIsData)
# Saída   : <output_dir>/time_series/sub-XXXX/tseries.csv
# Obs.: definir a variável atlas ("gordon" ou "glasser") e os caminhos no topo.

library(R.matlab)

# Configuration
input_dir <- ".\\ROIsData"  # Directory with MAT files
output_dir <- ".\\Arquivos\\GordonFiltered\\time_series"
atlas <- "gordon"

# Get all MAT files in input directory
mat_files <- list.files(
  path = input_dir,
  pattern = "^ROI_Subject.*\\.mat$",
  full.names = TRUE
)

# Create main output directory if it doesn't exist
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Process each file
for (mat_file in mat_files) {
  # Extract subject ID from filename
  sub_id <- gsub("^ROI_Subject(\\d+)_Session\\d+\\.mat$", "sub-\\1", basename(mat_file))
  sub_id <- sprintf("sub-%04d", as.integer(substring(sub_id, 5)))  # Format as sub-0001
  
  cat("Processing", sub_id, "\n")
  
  # Read MAT file
  mat_data <- readMat(mat_file)
  
  # Extract names
  nomes <- unlist(mat_data$names)
  
  # Identify atlas indices
  if(atlas == "gordon"){
    indices <- grepl("^atlasGordon", nomes)
  }
  if(atlas == "glasser"){
    indices <- grepl("^atlasGlasser", nomes)
  }
  
  # Create subject-specific output directory
  subject_output_dir <- file.path(output_dir, sub_id)
  if (!dir.exists(subject_output_dir)) {
    dir.create(subject_output_dir, recursive = TRUE)
  }
  
  # Process Gordon atlas
  if (atlas == "gordon") {
    process_atlas(indices, subject_output_dir, mat_data, nomes)
  }
  
  # Process Glasser atlas
  if (atlas == "glasser") {
    process_atlas(indices, subject_output_dir, mat_data, nomes)
  }
}

# Function to process each atlas
process_atlas <- function(indices, output_path, mat_data, names) {
  
  # Save time series
  time_series <- matrix(
    unlist(mat_data$data[indices]),
    nrow = sum(indices),
    byrow = TRUE
  )
  ts_file <- file.path(output_path, paste0("tseries.csv"))
  write.table(
    time_series,
    ts_file,
    sep = ",",
    row.names = FALSE,
    col.names = FALSE,
    quote = FALSE
  )
}

basic_files <- function(indices, suffix, output_path, mat_data, names){
  # Save ROI labels
  labels_file <- file.path(output_path, paste0("rois_labels_", suffix, ".txt"))
  writeLines(names[indices], labels_file)
  
  # Save coordinates
  coords <- matrix(
    as.numeric(unlist(mat_data$xyz[indices])),
    ncol = 3,
    byrow = TRUE
  )
  coords_file <- file.path(output_path, paste0("rois_coordinates_", suffix, ".csv"))
  write.table(
    coords,
    coords_file,
    sep = ",",
    row.names = FALSE,
    col.names = c("X", "Y", "Z"),
    quote = FALSE
  )
}


