from sklearn.metrics import classification_report
import torch


def _get_predictions(device, model, dataloader):
    # setting the model to evaluation mode
    model.eval()
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch in dataloader:
            b_input_ids, b_attention_mask, b_labels = [t.to(device) for t in batch]
            # forward pass to obtain model outputs
            outputs = model(b_input_ids, attention_mask=b_attention_mask)
            # extracting logits
            logits = outputs.logits
            # predicting the class with the highest score
            predicted_class = torch.argmax(logits, dim=1)
            # storing predictions and true labels for the current batch
            predictions.extend(predicted_class.cpu().numpy())
            true_labels.extend(b_labels.cpu().numpy())
    return predictions, true_labels


def _print_report(true_labels, baseline_predictions):
    print(classification_report(true_labels, baseline_predictions))
    report = classification_report(true_labels, baseline_predictions, output_dict=True)

    # labels = list(report.keys())[:-3]  # Exclude 'accuracy', 'macro avg', 'weighted avg'
    # precision = [report[label]['precision'] for label in labels]
    # recall = [report[label]['recall'] for label in labels]
    # f1_score = [report[label]['f1-score'] for label in labels]
    # support = [report[label]['support'] for label in labels]
    #
    # x = np.arange(len(labels))
    # width = 0.2
    #
    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width, precision, width, label='Precision', color='skyblue')
    # rects2 = ax.bar(x, recall, width, label='Recall', color='lightgreen')
    # rects3 = ax.bar(x + width, f1_score, width, label='F1 Score', color='salmon')
    #
    # ax.set_xlabel('Sentiment Class')
    # ax.set_ylabel('Scores')
    # ax.set_title('Classification Report After Fine-Tuning')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    # ax.legend()
    #
    # for i in range(len(support)):
    #     ax.text(i, max(precision[i], recall[i], f1_score[i]) + 0.02, f'Support: {support[i]}', ha='center', fontsize=9)
    #
    # ax.grid(False)
    #
    # fig.tight_layout()
    # plt.show()