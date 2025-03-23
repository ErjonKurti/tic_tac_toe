
import socket
import threading
from server.game_logic import check_winner, is_board_full

def start_server():
    """
    Nis serverin dhe prit lidhje nga klientët.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen()
    print("Serveri është startuar dhe pret lidhje...")

    clients = []
    players = ['X', 'O']

    def handle_game(client1, client2):
        """
        Menaxhon lojën midis dy klientëve.
        """
        board = [' ' for _ in range(9)]
        current_player = 0

        while True:
            
            client1.send(str.encode(' '.join(board)))
            client2.send(str.encode(' '.join(board)))

     
            move = clients[current_player].recv(1024).decode()
            board[int(move)] = players[current_player]

           
            if check_winner(board, players[current_player]):
                client1.send(str.encode(f"Player {players[current_player]} fiton!"))
                client2.send(str.encode(f"Player {players[current_player]} fiton!"))
                break

        
            if is_board_full(board):
                client1.send(str.encode("Barazim!"))
                client2.send(str.encode("Barazim!"))
                break

          
            current_player = 1 - current_player

        client1.close()
        client2.close()

    def accept_clients():
        """
        Prit dhe prano klientët.
        """
        while True:
            client, addr = server.accept()
            print(f"Lidhja u estabilizua me {addr}")
            clients.append(client)

            if len(clients) == 2:
                threading.Thread(target=handle_game, args=(clients[0], clients[1])).start()
                clients.clear()

    accept_clients()