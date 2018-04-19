library(ggplot2)
library(readr)

results <- read_tsv('label_type_results.tsv')

blue = "#4286f4"

ggplot(results, aes(x=label_type, y=accuracy)) +
  geom_point(col=blue, alpha=0.5, size=3) +
  ylim(0, 1) + 
  annotate("segment", x=0.5, xend=1.5, y=0.5, yend=0.5, color='red', size=1) +
  annotate("segment", x=1.5, xend=2.5, y=0.5, yend=0.5, color='red', size=1) +
  annotate("segment", x=2.5, xend=3.5, y=0.333, yend=0.333, color='red', size=1) +
  ggtitle("Comparison of Accuracy across\nTypes of Emotion Annotations") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))