
from pathlib import Path

import pandas as pd


# Dossiers du projet
DOSSIER_PROJET = Path(__file__).resolve().parent
DOSSIER_PROPRE = DOSSIER_PROJET / "donnees_brvm" / "propres"
DOSSIER_HISTORIQUE = DOSSIER_PROJET / "donnees_brvm" / "historique"

# Fichier historique central
FICHIER_HISTORIQUE = DOSSIER_HISTORIQUE / "historique_brvm.csv"


def construire_historique():
    # Rechercher toutes les collectes nettoyees
    fichiers = sorted(
        DOSSIER_PROPRE.glob("actions_nettoyees_*.csv")
    )

    if not fichiers:
        raise FileNotFoundError(
            "Aucun fichier nettoye trouve dans donnees_brvm/propres."
        )

    tableaux = []

    for fichier in fichiers:
        print(f"Lecture : {fichier.name}")

        df = pd.read_csv(
            fichier,
            encoding="utf-8-sig"
        )

        colonnes_obligatoires = {
            "Date_collecte",
            "Nom",
            "Dernier"
        }

        if not colonnes_obligatoires.issubset(df.columns):
            print("Fichier ignore : colonnes obligatoires absentes.")
            continue

        tableaux.append(df)

    if not tableaux:
        raise ValueError(
            "Aucun fichier ne contient les colonnes necessaires."
        )

    # Regrouper toutes les collectes
    historique = pd.concat(
        tableaux,
        ignore_index=True
    )

    # Eviter de compter deux fois une meme action
    # pour une meme date de collecte
    historique = historique.drop_duplicates(
        subset=["Date_collecte", "Nom"],
        keep="last"
    )

    # Trier par societe puis par date
    historique = historique.sort_values(
        by=["Nom", "Date_collecte"]
    ).reset_index(drop=True)

    # Creer le dossier de destination
    DOSSIER_HISTORIQUE.mkdir(
        parents=True,
        exist_ok=True
    )

    # Enregistrer l'historique complet
    historique.to_csv(
        FICHIER_HISTORIQUE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nHistorique construit avec succes.")
    print("Nombre de lignes :", len(historique))
    print("Nombre de societes :", historique["Nom"].nunique())
    print("Nombre de dates :", historique["Date_collecte"].nunique())
    print("Fichier :", FICHIER_HISTORIQUE)

    print("\nApercu :")
    print(historique.head(10).to_string(index=False))


if __name__ == "__main__":
    try:
        construire_historique()
    except Exception as erreur:
        print("\nErreur :", erreur)
