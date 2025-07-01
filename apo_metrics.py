from sklearn.metrics import cohen_kappa_score
import pandas as pd
import numpy as np


def lookup_score(turn: int, playa: str, dataset: list):
    """
    Get the scores for a specific turn/transcript
    """
    scores = {f"C-{i}": "N/A" for i in range(7)}
    for e in dataset["Annotations"]["AggregateHuman"]["TranscriptScores"]:
        if e["Turn"] == turn:
            if playa + "Scores" in e:
                scores = {k: e[playa + "Scores"][k] for k in scores.keys()}
                break
    def _conv(x):
        if x == "N/A":
            return x
        else:
            if np.isnan(x):
                return "N/A"
            else:
                return x
    _scores = {
        k: _conv(v) for k, v in scores.items()
    }
    _scores["Winner"] = dataset["Annotations"]["AggregateHuman"]["Winner"]
    return _scores


def normalise(arr: list, criterion: str):
    """
    Normalise scores for plotting. Criterion should be one of "C-{0-6}" or "Winner"
    """
    if criterion not in ["C-6", "Winner"]:
        new_arr = [x if not pd.isnull(x) else -1 for x in arr]
    elif criterion == "C-6":
        new_arr = [x if not pd.isnull(x) else -3 for x in arr]
    else:
        new_arr = []
        for x in arr:
            if type(x) == str:
                new_arr.append(x.capitalize())
            else:
                new_arr.append("Draw")
    return new_arr


def compute_weighted_kappa(column1: list, column2: list, labels: list, criterion: str):
    """
    Compute the weighted Cohen's kappa for two arrays corresponding
    to a given metric
    """
    def remap(x):
        if type(x) == str:
            return labels_from["Winner"].index(x.lower()) if x != "FAIL" else labels_from["Winner"].index("draw")
        else:
            return 2 # Draw
    
    def safe_remap(x):
        if type(x) == str:
            return int(x)
        return x

    if criterion == "Winner":
        labels = [0, 1, 2, -1]
        column1 = [remap(a) for a in column1]
        column2 = [remap(b) for b in column2]
    else:
        column1 = normalise([safe_remap(a) for a in column1], criterion)
        column2 = normalise([safe_remap(a) for a in column2], criterion)

    kappa = round(cohen_kappa_score(column1, column2, weights="linear", labels=labels), 3)
    return kappa, column1, column2


def compute_acc(responses, scores, version):
    accuracy, agreement = [], []
    for score, response in zip(scores, responses):
        if version == "7":
            if "Winner" not in response or "Winner" not in score:
                print(f"Error parsing response: {response} | score: {score}")
                response = {"Winner": "none"}
            if response["Winner"] is None:
                response = "none"
            accuracy.append(score["Winner"].lower() == response["Winner"].lower())
        else:
            accuracy.append(score[f"C-{version}"] == response[f"C-{version}"])
    accuracy = sum(accuracy)*100/len(accuracy)
    return accuracy #, agreement

