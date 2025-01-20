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

