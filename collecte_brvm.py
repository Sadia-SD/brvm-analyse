
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
from io import StringIO


# Adresse de la page des actions BRVM
URL = "https://www.sikafinance.com/marches/aaz"

# Dossier du projet
DOSSIER_PROJET = Path(__file__).resolve().parent
DOSSIER_BRUT = DOSSIER_PROJET / "donnees_brvm" / "brutes"


def collecter_brvm():
    maintenant = datetime.now()
    date_collecte = maintenant.strftime("%Y-%m-%d")

    print("Connexion a Sika Finance...")

    reponse = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    reponse.raise_for_status()

    print("Page recuperee. Lecture du tableau des actions...")

    tableaux = pd.read_html(StringIO(reponse.text))

    colonnes_requises = {
        "nom",
        "ouverture",
        "+haut",
        "+bas",
        "volume (titres)",
        "volume (xof)",
        "dernier",
        "variation"
    }

    tableau_actions = None

    for tableau in tableaux:
        colonnes = {
            str(colonne).strip().lower()
            for colonne in tableau.columns
        }

        if colonnes_requises.issubset(colonnes):
            tableau_actions = tableau.copy()
            break

    if tableau_actions is None:
        raise ValueError(
            "Le tableau des actions BRVM est introuvable."
        )

    if len(tableau_actions) < 40:
        raise ValueError(
            f"Collecte suspecte : seulement "
            f"{len(tableau_actions)} lignes recuperees."
        )

    # Ajouter la date de collecte
    tableau_actions.insert(0, "Date_collecte", date_collecte)

    # Creer le dossier si necessaire
    DOSSIER_BRUT.mkdir(parents=True, exist_ok=True)

    # Un seul fichier brut par jour
    fichier = DOSSIER_BRUT / f"actions_{date_collecte}.csv"

    # Une nouvelle collecte du meme jour remplace le fichier du jour
    tableau_actions.to_csv(
        fichier,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCollecte reussie !")
    print("Date de collecte :", date_collecte)
    print("Nombre de lignes :", len(tableau_actions))
    print("Fichier brut :", fichier)
    print("Les fichiers des autres jours sont conserves.")


if __name__ == "__main__":
    try:
        collecter_brvm()
    except Exception as erreur:
        print("\nErreur pendant la collecte :", erreur)
