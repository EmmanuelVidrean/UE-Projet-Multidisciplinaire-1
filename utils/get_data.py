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


if __name__ == "__main__":
    iris_df = load_unesco_data()
    print(iris_df.head())
    print("\nColonnes disponibles :", iris_df.columns.tolist())
