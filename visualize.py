import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# get delicious data
def load_test_data(filename="testdaten.json"):
    with open(filename, "r") as f:
        return json.load(f)

# check for outliers (usually around 2 * std_dev)
def detect_outliers(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    threshold_upper = mean + 2 * std_dev
    threshold_lower = mean - 2 * std_dev
    outliers = [x for x in data if x < threshold_lower or x > threshold_upper]
    return outliers, threshold_lower, threshold_upper

# Visualize distribution
def visualize_data(filename="testdaten.json"):
    # Daten laden
    dataset = load_test_data(filename)

    # check for relevant data, hier it's ortsteile
    ortsteile = set([entry["ortsteil"] for entry in dataset])

    for ortsteil in ortsteile:
        # get data from ortsteile
        values = [entry["value"] for entry in dataset if entry["ortsteil"] == ortsteil]

        # Histogramm und KDE erstellen
        plt.figure(figsize=(10, 6))
        sns.histplot(values, kde=True, color="blue", stat="density", bins=30, label=f"Wert der Einheiten ({ortsteil})")

        # integration of outliers check
        outliers, threshold_lower, threshold_upper = detect_outliers(values)

        # mark those lil buggers
        plt.scatter(outliers, [0] * len(outliers), color="red", label="Ausreißer", zorder=5)

        # show "schwellenwert" ... whats this in eng again?
        plt.axvline(x=threshold_lower, color="red", linestyle="--", label="Unterer Ausreißerschwellenwert")
        plt.axvline(x=threshold_upper, color="red", linestyle="--", label="Oberer Ausreißerschwellenwert")

        # nothing but labels and titels
        plt.title(f"Verteilung der Einheitswerte und Ausreißer ({ortsteil})")
        plt.xlabel("Wert der Einheit")
        plt.ylabel("Dichte")

        # Legende anzeigen
        plt.legend()
        plt.show()

# Hauptausführung
if __name__ == "__main__":
    visualize_data()