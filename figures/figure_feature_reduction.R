library(readr)
library(tidyr)
library(dplyr)
library(ggplot2)

results <- read_tsv('feature_reduction_results.tsv') 

blue = "#4286f4"

ggplot(results, aes(x=factor(feature_percentile), y=accuracy)) +
  geom_count(col=blue, alpha=0.5, size=3) +
  geom_abline(intercept=0.33, slope=0, col="red") +
  ggtitle("Comparison of % Features Used in SVC") +
  ylim(0, 1) + 
  theme_minimal() +
  xlab("% voxels used as features")

# ggplot(results, aes(feature_percentile, accuracy)) +
#   geom_col() +
#   theme_minimal()