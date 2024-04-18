# 1. predict
# 2. calculate_metrics
# 3. save result

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tabulate import tabulate
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Filter out INFO-level messages


def prediction_and_casting(ner_model, dataset, mapping):
    all_true_tag_ids, all_predicted_tag_ids = [], []

    for x, y in dataset:
        if len(x[0]) > 3135:
            continue
        output = ner_model.predict(x, verbose=0)
        predictions = np.argmax(output, axis=-1)
        predictions = np.reshape(predictions, [-1])

        true_tag_ids = np.reshape(y, [-1])

        mask = (true_tag_ids > 0) & (predictions > 0)
        true_tag_ids = true_tag_ids[mask]
        predicted_tag_ids = predictions[mask]

        all_true_tag_ids.append(true_tag_ids)
        all_predicted_tag_ids.append(predicted_tag_ids)

    all_true_tag_ids = np.concatenate(all_true_tag_ids)
    all_predicted_tag_ids = np.concatenate(all_predicted_tag_ids)

    predicted_tags = [mapping[tag] for tag in all_predicted_tag_ids]
    real_tags = [mapping[tag] for tag in all_true_tag_ids]

    return predicted_tags, real_tags

def calculate_metrics(y_true, y_pred, labels):
    # Mapping labels to numeric indices
    label_to_index = {label: idx for idx, label in enumerate(labels)}
    index_to_label = {idx: label for label, idx in label_to_index.items()}
    y_true_mapped = [label_to_index[label] for label in y_true]
    y_pred_mapped = [label_to_index[label] for label in y_pred]

    # Overall metrics
    accuracy = accuracy_score(y_true_mapped, y_pred_mapped)
    precision = precision_score(y_true_mapped, y_pred_mapped, average='weighted', zero_division=0)
    recall = recall_score(y_true_mapped, y_pred_mapped, average='weighted', zero_division=0)  # Set zero_division to 0
    f1 = f1_score(y_true_mapped, y_pred_mapped, average='weighted')

    # Per-label metrics
    per_label_accuracy = {}
    per_label_precision = {}
    per_label_recall = {}
    per_label_f1 = {}

    for label in labels:
        label_indices = [i for i, true_label in enumerate(y_true) if true_label == label]
        if len(label_indices) > 0:
            per_label_accuracy[label] = accuracy_score([y_true_mapped[i] for i in label_indices], [y_pred_mapped[i] for i in label_indices])
            per_label_precision[label] = precision_score([y_true_mapped[i] for i in label_indices], [y_pred_mapped[i] for i in label_indices], average='weighted', zero_division=0)
            per_label_recall[label] = recall_score([y_true_mapped[i] for i in label_indices], [y_pred_mapped[i] for i in label_indices], average='weighted', zero_division=0)  # Set zero_division to 0
            per_label_f1[label] = f1_score([y_true_mapped[i] for i in label_indices], [y_pred_mapped[i] for i in label_indices], average='weighted', zero_division=0)
        else:
            per_label_accuracy[label] = 0
            per_label_precision[label] = 0
            per_label_recall[label] = 0
            per_label_f1[label] = 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'per_label_accuracy': per_label_accuracy,
        'per_label_precision': per_label_precision,
        'per_label_recall': per_label_recall,
        'per_label_f1': per_label_f1,
        'index_to_label': index_to_label
    }

def evaluate_model(ner_model, val_data, mapping, filepath):
    y_pred, y_val = prediction_and_casting(ner_model, val_data, mapping)
    #labels
    labels = mapping.values()
    metrics = calculate_metrics(y_val, y_pred, labels)

    # Constructing table
    table_data = []
    for label in labels:
        table_data.append([label,
                        metrics['per_label_accuracy'][label],
                        metrics['per_label_precision'][label],
                        metrics['per_label_recall'][label],
                        metrics['per_label_f1'][label]])
    overall_accuracy = calculate_metrics(y_val, y_pred, labels)

    table = tabulate(table_data, headers=["Label", "Accuracy", "Precision", "Recall", "F1-score"], tablefmt="grid")
    # Saving results into a text file
    directory = os.path.dirname(filepath)
    file_count = len(os.listdir(directory))
    filepath = f"{directory}/model_evaluate_{file_count}.txt"
    
    with open(filepath, "w") as f:
        f.write("Overall Accuracy:".ljust(20) + str(overall_accuracy['accuracy']) + "\n")
        f.write("Overall Precision:".ljust(20) + str(overall_accuracy['precision']) + "\n")
        f.write("Overall Recall:".ljust(20) + str(overall_accuracy['recall']) + "\n")
        f.write("Overall F1-score:".ljust(20) + str(overall_accuracy['f1']) + "\n")
        f.write(table)

    return 'Evaluation results saved successfully in ' + filepath
