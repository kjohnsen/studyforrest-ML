library(ggplot2)
library(readr)
library(tidyr)

results <- read_tsv('multivoxel_svm_results.tsv')

results <- gather(results, key=cv_fold, value=accuracy, -subject, -strategy, -label_type)

blue = "#4286f4"

ggplot(results, aes(subject, accuracy)) +
  geom_boxplot(fill=blue, alpha=0.5) +
  geom_abline(intercept=0.333, slope=0, col="red") +
  ggtitle("Linear SVM Cross-validation Scores") +
  ylim(0, 1) +
  theme_minimal()

# alpha_val = 0.0


# ggplot(results, aes(x=subject)) +
#   #geom_col(aes(y=max), fill='#f45c42') +
#   geom_col(aes(y=cv1), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv2), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv3), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv4), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv5), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv6), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv7), col="#4286f4", alpha=alpha_val) +
#   geom_col(aes(y=cv8), col="#4286f4", alpha=alpha_val) +
#   ylab('Prediction accuracy') + 
#   theme_minimal() + 
#   ggtitle('Accuracy for SVM arousal prediction across 5 subjects')
