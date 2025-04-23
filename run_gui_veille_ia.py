# run_gui_veille_ia.py

import tkinter as tk
import subprocess
import threading

def lancer_pipeline():
    bouton.config(state=tk.DISABLED)
    label_status.config(text="Lancement de la veille automatique...")

    def run():
        process = subprocess.Popen(["python", "auto_run.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        # Affiche les logs dans la zone texte
        text_output.insert(tk.END, stdout + "\n")
        if stderr:
            text_output.insert(tk.END, "Erreur :\n" + stderr)

        bouton.config(state=tk.NORMAL)
        label_status.config(text="Traitement terminé.")

    threading.Thread(target=run).start()

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Veille IA & Vente – Agrégateur Automatique")
fenetre.geometry("700x450")

label_status = tk.Label(fenetre, text="Surveille automatiquement les dernières actualités IA & Vente", font=("Arial", 12))
label_status.pack(pady=10)

bouton = tk.Button(fenetre, text="Lancer la surveillance", command=lancer_pipeline, bg="green", fg="white", font=("Arial", 12, "bold"))
bouton.pack(pady=10)

text_output = tk.Text(fenetre, height=20, width=90)
text_output.pack(padx=10, pady=10)

fenetre.mainloop()
