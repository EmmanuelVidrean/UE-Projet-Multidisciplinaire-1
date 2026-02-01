import os
import pandas as pd
import re
from html import unescape

# commande pour tester cette fonction:
# python -m doctest -v src/utils/clean_data.py

def clean_html_text(text):
    """
    Nettoie une chaîne de texte :
    - décode les entités HTML (&nbsp;, &amp;, etc.)
    - supprime les balises HTML (<em>, <b>, <i>, ...)
    - normalise les espaces.

    """
    # 1) Décodage des entités HTML (&nbsp; -> \xa0, etc.)
    text = unescape(text)

    # 2) Suppression des balises HTML
    # Exemple: "<em>Site</em>" -> "Site"
    text = re.sub(r"<[^>]*>", "", text)

    # 3) Remplacement des espaces insécables (\xa0) par des espaces classiques
    text = text.replace("\xa0", " ")

    # 4) Nettoyage des espaces multiples
    text = " ".join(text.split())

    return text

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

    # Nettoyage de la description courte si la colonne existe
    if 'short_description_en' in df.columns:
        df['short_description_en'] = df['short_description_en'].apply(clean_html_text)
    
    # Nettoyage de name_en  si la colonne existe
    if 'name_en' in df.columns:
        df['name_en'] = df['name_en'].apply(clean_html_text)

    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

    # Sauvegarder les données nettoyées
    df.to_csv(cleaned_path, index=False)

    return df

if __name__ == "__main__":
    clean_data()