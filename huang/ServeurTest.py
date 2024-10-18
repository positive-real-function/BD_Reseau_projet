import socket

# Créer un objet socket en utilisant l'adresse IPv4 et le protocole TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associer le socket à une adresse IP et un numéro de port spécifiques
server_socket.bind(("127.0.0.1", 8008))

# Définir le socket en mode d'écoute, avec un nombre maximum de connexions en attente de 5
server_socket.listen(5)
print("Serveur en écoute sur 127.0.0.1:8008")

# Valeurs par défaut pour tester sans base de données
users_data = {
    "admin": {"is_admin": 1, "room_number": None, "portid": "1001", "caretid": "abcd1234"},
    "user1": {"is_admin": 0, "room_number": "101", "portid": "1001", "caretid": "abcd1234"}
}

# Boucle infinie pour accepter et traiter les connexions client
while True:
    # Accepter une nouvelle connexion client
    conn, address = server_socket.accept()
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
    
    # Utiliser les données par défaut à la place de la base de données
    user = users_data.get(username)
    
    if user:
        if user["is_admin"] == 1:
            # Si l'utilisateur est un administrateur, vérifier que portid et caretid sont corrects
            if user["portid"] == portid and user["caretid"] == caretid:
                response = "Bienvenue ！ L'accès est autorisé."
            else:
                response = "Erreur ： portid ou caretid incorrect."
        else:
            # Si l'utilisateur n'est pas un administrateur, vérifier toutes les informations
            if user["room_number"] == room_number and user["portid"] == portid and user["caretid"] == caretid:
                response = "Bienvenue ！ L'accès est autorisé."
            else:
                response = "Erreur ： numéro de salle, portid ou caretid incorrect."
    else:
        response = "Utilisateur inconnu."
    
    # Envoyer la réponse au client
    conn.sendall(bytes(response, encoding="utf-8"))
    
    # Fermer la connexion client
    conn.close()
