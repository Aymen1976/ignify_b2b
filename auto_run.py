# auto_run.py

import time
import subprocess

PAUSE_MINUTES = 1  # Pause entre chaque relance automatique

print("=== Lancement automatique du pipeline IA & Vente ===")

while True:
    try:
        subprocess.run(["python", "main.py"], check=True)
        print("=== Traitement terminé ===\n")
    except Exception as e:
        print("Erreur durant le traitement :", e)

    print(f"Nouvelle surveillance dans {PAUSE_MINUTES} minute(s)...\n")
    time.sleep(PAUSE_MINUTES * 60)
