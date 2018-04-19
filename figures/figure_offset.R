library(ggplot2)
library(tidyr)
library(readr)
library(dplyr)

results <- read_tsv('offset_results.tsv', col_names = T)

blue = "#4286f4"

ggplot(results, aes(subject, accuracy)) +
  geom_col( aes(fill=offset), position='dodge') +
  geom_abline(slope=0, intercept=0.33, color='red') +
  ggtitle('Effect of Hemodynamic Response Delay Offset on SVC Accuracy') + 
  ylim(0, 1) +
  theme_minimal()