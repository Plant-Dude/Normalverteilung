import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Funktion zur Generierung von Einheiten pro Ortsteil
def generate_unit(ortsteil, data):
    """
    Generiert Einheiten für einen bestimmten Ortsteil basierend auf den gegebenen Daten.

    Args:
        ortsteil (str): Der Name des Ortsteils.
        data (dict): Daten wie Mittelwert und Standardabweichung für die Wertgenerierung.

    Returns:
        list: Eine Liste mit Einheiten für den Ortsteil.
    """
    n = data.get("num_units", 250)  # Anzahl der Einheiten (Standard: 250)
    mean = data.get("mean", 3200)  # Durchschnittswert pro m²
    std_dev = data.get("std_dev", 500)  # Standardabweichung

    units = []
    for i in range(1, n + 1):
        unit_name = f"{ortsteil}_Unit_{i}"
        value = round(random.gauss(mean, std_dev))  # Normalverteilung
        units.append({"name": unit_name, "ortsteil": ortsteil, "value": max(1500, value)})  # Mindestwert
    return units


# Testdaten generieren und speichern
def save_test_data(filename="testdaten.json"):
    """
    Erstellt Testdaten für verschiedene Ortsteile und speichert sie in einer Datei.
    """
    # Auslesen von list_district.json
    try:
        with open("list_district.json", "r") as f:
            ortsteile_data = json.load(f)
    except FileNotFoundError:
        print("Nöpe, Datei net gfunne.")
        return

    # "Berechnung" der Standardabweichung basierend auf sqm_base_price!
    # außerordentliche Abweichung vllt bei Krise/Chaos
    desired_percent = 15

    for ortsteil in ortsteile_data:
        mean = ortsteil.get("sm_base_price")
        if mean:
            ortsteil["std_dev"] = (desired_percent / 100) * mean # Berechnung der Standardabweichung

    all_units = []
    for ortsteil in ortsteile_data:
        units = generate_unit(ortsteil["ortsteil"], ortsteil)
        all_units.extend(units)

    # Speichern in Datei
    with open(filename, "w") as f:
        json.dump(all_units, f, indent=4)
    print(f"Testdaten wurden in '{filename}' gespeichert.")

# Hauptausführung
if __name__ == "__main__":
    save_test_data()

### Generate units, tits code from the other project but prbly needed in order for things to get smoothly

def generate_unit(ortsteil, data):
    # Ortsteil-Daten aus JSON extrahieren
    district_data = next((d for d in data if d ["ortsteil"] == ortsteil), None)
    if not district_data:
        raise ValueError(f"Nöp, data {ortsteil} not found.")

    district = district_data["district"]
    value_cat = district_data["value_cat"]
    sm_base_price = district_data["sm_base_price"]

    # Größe basierend auf Gaußscher Normalverteilung
    mean_size = 20 + value_cat * (180 - 20) # Scheitelpunkunkt basiernend auf value_cat
    std_dev_size = 20 # Standardabweichung für ralistische Verteilung
    size = max(20, min(int(np.random.normal(mean_size, std_dev_size)), 180)) # Begrenzung auf [20, 180]

    # Zustand basierend auf value_cat
    condition_min = max(0.1, value_cat - 0.2)
    condition_max = min(1.0, value_cat + 0.2)
    condition = np.random.uniform(condition_min, condition_max)

    # Extras basierend auf value_cat
    extras_probability = round(0.05 + value_cat * 0.15, 2)
    extras = 1 if random.random() < extras_probability else 0

    # Wert berechnen (nach Tests vielleicht auch über Normalverteilung
    value = calculate_value(size, condition,extras, sm_base_price)

    # Einheit erstellen
    name = generate_unit_name()
    return RealEstateUnit(name, district, value, size, condition, extras, rent=None, tenant=None)


