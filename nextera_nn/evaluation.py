from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np


baseline_predictions, true_labels = get_predictions(model, test_dataloader)

print(classification_report(true_labels, baseline_predictions))
report = classification_report(true_labels, baseline_predictions, output_dict=True)

labels = list(report.keys())[:-3]  # Exclude 'accuracy', 'macro avg', 'weighted avg'
precision = [report[label]['precision'] for label in labels]
recall = [report[label]['recall'] for label in labels]
f1_score = [report[label]['f1-score'] for label in labels]
support = [report[label]['support'] for label in labels]

x = np.arange(len(labels))
width = 0.2

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, precision, width, label='Precision', color='skyblue')
rects2 = ax.bar(x, recall, width, label='Recall', color='lightgreen')
rects3 = ax.bar(x + width, f1_score, width, label='F1 Score', color='salmon')

ax.set_xlabel('Sentiment Class')
ax.set_ylabel('Scores')
ax.set_title('Classification Report After Fine-Tuning')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

for i in range(len(support)):
    ax.text(i, max(precision[i], recall[i], f1_score[i]) + 0.02, f'Support: {support[i]}', ha='center', fontsize=9)

ax.grid(False)

fig.tight_layout()
plt.show()