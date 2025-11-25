import os
import pandas as pd

def load_unesco_data():
    """
    Charge le fichier CSV
    Retourne un DataFrame
    """
    # Récupération du csv à partir de l'arborecence du projet
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "whc-sites-2019 - whc-sites-2019.csv")

    # Lecture du fichier CSV avec pandas
    data_frame = pd.read_csv(data_path)

    return data_frame

def get_all_unique_numbers():
    """
    Retourne la liste de tous les 'unique_number' présents dans le dataset
    """
    df = load_unesco_data()
    unique_numbers = df["unique_number"].dropna().tolist()
    return unique_numbers

def get_site_by_unique_number(unique_number):
    """
    Prend en parametre un unique number
    Retourne un dictionnaire représentant le site correspondant
    """
    df = load_unesco_data()

    # Filtrer les lignes correspondant à ce numéro unique
    result = df[df["unique_number"] == unique_number]

    if result.empty:
        print(f"Aucun site trouvé avec unique_number = {unique_number}")
        return None

    return result.iloc[0].to_dict()

def get_coords_dict(unique_numbers):
    """
    Prend en parametre une liste de unique number
    Retourne un dictionnaire {unique_number: (longitude, latitude)}
    """
    df = load_unesco_data()

    # Sélection des colonnes utiles
    subset = df.loc[:, ["unique_number", "longitude", "latitude"]].copy()

    # Conversion en valeurs numériques
    subset["unique_number"] = pd.to_numeric(subset["unique_number"], errors="coerce") # coerce convertit les valeurs invalides en NaN
    subset["longitude"] = pd.to_numeric(subset["longitude"], errors="coerce")
    subset["latitude"]  = pd.to_numeric(subset["latitude"],  errors="coerce")

    #suppression des lignes avec NaN et doublons
    subset = (
        subset.dropna(subset=["unique_number", "longitude", "latitude"])
              .drop_duplicates(subset=["unique_number"])
              .set_index("unique_number")
    )

    # Construction du dictionnaire
    result = {}
    for num in unique_numbers:
        try:
            key = float(num)
        except Exception:
            continue

        if key in subset.index:
            row = subset.loc[key]
            result[int(key)] = (float(row["longitude"]), float(row["latitude"]))

    return result

def get_all_categories():
    """
    Retourne la liste de toutes les catégories
    """
    df = load_unesco_data()

    # On récupère les catégories uniques
    categories = (
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    return categories

def get_all_states_name():
    """
    Retourne la liste de tous les pays
    """
    df = load_unesco_data()

    # On garde uniquement les lignes où transboundary == 0
    df_non_transboundary = df[df["transboundary"] == 0]

    categories = (
        df_non_transboundary["states_name_en"]
        .dropna()           
        .unique()           
        .tolist()         
    )

    return categories

def get_all_region_name():
    """
    Retourne la liste de tous les region
    """
    df = load_unesco_data()

    # On garde uniquement les lignes où transboundary == 0
    df_non_transboundary = df[df["transboundary"] == 0]

    categories = (
        df_non_transboundary["region_en"]
        .dropna()           
        .unique()           
        .tolist()         
    )

    return categories

def get_unique_numbers_by_category(category_name):
    """
    Retourne la liste des 'unique_number' correspondant à une catégorie donnée.
    """
    df = load_unesco_data()

    # On filtre les lignes correspondant exactement à la catégorie donnée
    filtered_df = df[df["category"] == category_name]

    unique_numbers = (
        filtered_df["unique_number"]
        .dropna()
        .unique()
        .tolist()
    )

    return unique_numbers

def get_unique_numbers_by_state(state_name):
    """
    Retourne la liste des 'unique_number' correspondant au pays donnée.
    """
    df = load_unesco_data()

    # On filtre les lignes correspondant exactement au pays donnée
    filtered_df = df[df["states_name_en"] == state_name]

    unique_numbers = (
        filtered_df["unique_number"]
        .dropna()
        .unique()
        .tolist()
    )

    return unique_numbers

def get_unique_numbers_by_region(region_name):
    """
    Retourne la liste des 'unique_number' correspondant au region donnée.
    """
    df = load_unesco_data()

    # On filtre les lignes correspondant exactement au region donnée
    filtered_df = df[df["region_en"] == region_name]

    unique_numbers = (
        filtered_df["unique_number"]
        .dropna()
        .unique()
        .tolist()
    )

    return unique_numbers