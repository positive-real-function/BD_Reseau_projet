# Importer la bibliothèque socket
import socket
# Importer la bibliothèque sqlite3
import sqlite3

# Créer un objet socket en utilisant l'adresse IPv4 et le protocole TCP
x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associer le socket à une adresse IP et un numéro de port spécifiques
x.bind(("127.0.0.1", 8008))

# Définir le socket en mode d'écoute, avec un nombre maximum de connexions en attente de 5
x.listen(5)

# Se connecter à la base de données
conn_db = sqlite3.connect('database.db')
cursor = conn_db.cursor()

# Boucle infinie pour accepter et traiter les connexions client
while True:
    # Accepter une nouvelle connexion client
    conn, address = x.accept()
    # Afficher les informations de l'adresse du client
    print("Nouvelle connexion de ", address)
    
    try:
        # Recevoir les données envoyées par le client avec un délai de 5 secondes
        conn.settimeout(5)
        data = conn.recv(1024).decode("utf-8")
        username, room_number, portid, caretid = data.split(',')
    except socket.timeout:
        print("Connexion fermée car pas de données reçues")
        conn.close()
        continue
    
    # Vérifier si l'utilisateur est un administrateur
    cursor.execute("SELECT is_admin FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    if user and user[0] == 1:
        # Si l'utilisateur est un administrateur, vérifier que portid et caretid sont corrects, sans vérifier room_number
        cursor.execute("SELECT portid, caretid FROM users WHERE username=?", (username,))
        correct_data = cursor.fetchone()
        
        if correct_data and correct_data[0] == portid and correct_data[1] == caretid:
            response = "Bienvenue ！ L'accès est autorisé."
        else:
            response = "Erreur ： portid ou caretid incorrect."
    else:
        # Si l'utilisateur n'est pas un administrateur, vérifier que room_number, portid et caretid sont corrects
        cursor.execute("SELECT room_number, portid, caretid FROM users WHERE username=?", (username,))
        correct_data = cursor.fetchone()
        
        if correct_data and correct_data[0] == room_number and correct_data[1] == portid and correct_data[2] == caretid:
            response = "Bienvenue ！ L'accès est autorisé."
        else:
            response = "Erreur ： numéro de salle, portid ou caretid incorrect."
    
    # Envoyer la réponse au client
    conn.sendall(bytes(response, encoding="utf-8"))
    
    # Fermer la connexion client
    conn.close()

# Fermer la connexion à la base de données
conn_db.close()

