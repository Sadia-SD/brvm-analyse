
from pathlib import Path
import pandas as pd


# Dossiers du projet
DOSSIER_PROJET = Path(__file__).resolve().parent
DOSSIER_BRUT = DOSSIER_PROJET / "donnees_brvm" / "brutes"
DOSSIER_PROPRE = DOSSIER_PROJET / "donnees_brvm" / "propres"


def convertir_nombre(valeur):
    """Convertit un nombre contenant des espaces en nombre numerique."""
    if pd.isna(valeur):
        return None

    texte = str(valeur).strip()
    texte = (
        texte.replace("\u00a0", "")
        .replace("\u202f", "")
        .replace(" ", "")
    )

    if texte in ("", "-", "—"):
        return None

    texte = texte.replace(",", ".")

    try:
        return float(texte)
    except ValueError:
        return None


def convertir_variation(valeur):
    """Convertit une variation en pourcentage numerique."""
    if pd.isna(valeur):
        return None

    texte = str(valeur).strip()
    texte = (
        texte.replace("\u00a0", "")
        .replace("\u202f", "")
        .replace(" ", "")
        .replace("%", "")
        .replace(",", ".")
    )

    try:
        return float(texte)
    except ValueError:
        return None


def preparer_donnees():
    fichiers = sorted(DOSSIER_BRUT.glob("actions_*.csv"))

    if not fichiers:
        raise FileNotFoundError(
            "Aucun fichier brut trouve dans donnees_brvm/brutes."
        )

    DOSSIER_PROPRE.mkdir(parents=True, exist_ok=True)

    print("Preparation des donnees BRVM...")

    for fichier_source in fichiers:
        # Extraire la date du nom du fichier brut
        date_collecte = fichier_source.stem.replace("actions_", "")

        # Ignorer les anciens fichiers dont le nom contient encore une heure
        if len(date_collecte) != 10:
            print(
                f"Ancien format ignore : {fichier_source.name}"
            )
            continue

        print(f"\nTraitement : {fichier_source.name}")

        df = pd.read_csv(
            fichier_source,
            encoding="utf-8-sig",
            dtype=str
        )

        # Ajouter la date si elle n'existe pas deja
        if "Date_collecte" not in df.columns:
            df.insert(0, "Date_collecte", date_collecte)
        else:
            df["Date_collecte"] = date_collecte

        colonnes_numeriques = [
            "Ouverture",
            "+Haut",
            "+Bas",
            "Volume (titres)",
            "Volume (XOF)",
            "Dernier"
        ]

        for colonne in colonnes_numeriques:
            if colonne in df.columns:
                df[colonne] = df[colonne].apply(convertir_nombre)

        if "Variation" in df.columns:
            df["Variation"] = df["Variation"].apply(
                convertir_variation
            )

        if "Nom" not in df.columns:
            print("Fichier ignore : colonne Nom absente.")
            continue

        df = df.dropna(subset=["Nom"])

        # Un fichier propre par jour
        fichier_sortie = (
            DOSSIER_PROPRE
            / f"actions_nettoyees_{date_collecte}.csv"
        )

        df.to_csv(
            fichier_sortie,
            index=False,
            encoding="utf-8-sig"
        )

        print("Lignes conservees :", len(df))
        print("Fichier propre :", fichier_sortie)

    print("\nPreparation terminee.")


if __name__ == "__main__":
    try:
        preparer_donnees()
    except Exception as erreur:
        print("\nErreur pendant la preparation :", erreur)
