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

def get_site_by_unique_number(unique_number):
    df = load_unesco_data()

    # Filtrer les lignes correspondant à ce numéro unique
    result = df[df["unique_number"] == unique_number]

    if result.empty:
        print(f"Aucun site trouvé avec unique_number = {unique_number}")
        return None

    return result.iloc[0].to_dict()


if __name__ == "__main__":
    site = get_site_by_unique_number(230)
    if site:
        for key, value in site.items():
            print(f"{key}: {value}")
