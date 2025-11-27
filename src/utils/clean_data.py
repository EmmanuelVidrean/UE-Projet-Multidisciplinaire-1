import os
import pandas as pd

# commande pour tester cette fonction:
# python -m doctest -v src/utils/clean_data.py

def clean_data():
    """
    Nettoie les données brutes et sauvegarde les données nettoyées.

    >>> df = clean_data()
    >>> type(df).__name__
    'DataFrame'
    >>> len(df) > 0
    True
    >>> 'longitude' in df.columns
    True
    >>> 'latitude' in df.columns
    True
    """
    # Chemin vers les données brutes
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "whc-sites-2019 - whc-sites-2019.csv")
    cleaned_path = os.path.join(base_dir, "data", "cleaned", "cleaned_data.csv")

    # Charger les données
    df = pd.read_csv(raw_path)

    # Nettoyer : supprimer les lignes avec coordonnées manquantes
    df = df.dropna(subset=['longitude', 'latitude'])

    # Convertir les colonnes numériques
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['area_hectares'] = pd.to_numeric(df['area_hectares'], errors='coerce')

    # Supprimer les lignes avec NaN après conversion
    df = df.dropna(subset=['longitude', 'latitude'])

    # Sauvegarder les données nettoyées
    df.to_csv(cleaned_path, index=False)

    return df

if __name__ == "__main__":
    clean_data()