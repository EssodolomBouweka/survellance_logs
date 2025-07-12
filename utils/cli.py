def show_menu():
    """
    Affiche le menu principal de l'application en mode CLI (ligne de commande),
    puis récupère le choix de l'utilisateur.

    :return: Chaîne de caractères correspondant au choix utilisateur
    """
    print("==============================")
    print(" SYSTÈME DE SURVEILLANCE CLI")
    print("==============================")
    print("1. Lancer le traitement des logs")          # Option pour démarrer l’analyse des logs
    print("2. Afficher les alertes détectées")         # Option pour afficher les alertes déjà identifiées
    print("3. Générer le rapport PDF")                  # Option pour créer le rapport PDF des stats
    print("4. Générer la visualisation statistique")   # Option pour créer les graphiques de stats
    print("5. Quitter")                                # Option pour quitter le programme
    
    # Demande à l’utilisateur de saisir son choix
    return input("\nVeuillez choisir une option (1-5) : ")


# === Test rapide de la fonction CLI si ce script est exécuté directement ===
if __name__ == "__main__":
    choice = show_menu()
    # Affiche le choix de l’utilisateur (utile pour débug ou test manuel)
    print(f"Vous avez choisi l'option : {choice}")
    
    # Ici, tu peux ajouter des tests supplémentaires ou appeler d'autres fonctions
