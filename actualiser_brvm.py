
from pathlib import Path
import subprocess
import sys


# Dossier principal du projet
DOSSIER_PROJET = Path(__file__).resolve().parent

# Scripts a executer dans l'ordre
SCRIPTS = [
    ("1/3 - Collecte des donnees BRVM", "collecte_brvm.py"),
    ("2/3 - Nettoyage des donnees", "preparer_brvm.py"),
    ("3/3 - Construction de l'historique", "historique_brvm.py"),
]


def executer_script(etape, nom_script):
    chemin_script = DOSSIER_PROJET / nom_script

    print("\n" + "=" * 60, flush=True)
    print(etape, flush=True)
    print("=" * 60, flush=True)

    if not chemin_script.exists():
        print(f"ERREUR : fichier introuvable : {chemin_script}")
        return False

    resultat = subprocess.run(
        [sys.executable, str(chemin_script)],
        cwd=DOSSIER_PROJET
    )

    if resultat.returncode != 0:
        print(f"\nECHEC : {nom_script}")
        print("Le processus est interrompu.")
        return False

    print(f"\nEtape terminee : {nom_script}", flush=True)
    return True


def main():
    print("ACTUALISATION AUTOMATIQUE BRVM", flush=True)

    for etape, nom_script in SCRIPTS:
        if not executer_script(etape, nom_script):
            print("\nActualisation interrompue.", flush=True)
            return

    print("\n" + "=" * 60, flush=True)
    print("ACTUALISATION TERMINEE AVEC SUCCES", flush=True)
    print("Les fichiers des jours precedents sont conserves.")
    print("L'historique a ete reconstruit depuis les fichiers propres.")
    print("=" * 60, flush=True)


if __name__ == "__main__":
    main()
