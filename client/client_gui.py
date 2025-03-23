from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QGridLayout, QWidget, QLabel
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette
import socket
import threading

class TicTacToeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe | By Erjon Kurti")
        self.setGeometry(100, 100, 400, 450)
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 5555))
        self.init_ui()
        self.receive_updates()

    def init_ui(self):
        """
        Krijon ndërfaqen grafike të lojës.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        self.title_label = QLabel("Tic Tac Toe", self)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #333333;")
        layout.addWidget(self.title_label, 0, 0, 1, 3)

    
        self.buttons = []
        for i in range(9):
            button = QPushButton(' ', self)
            button.setFixedSize(QSize(100, 100))
            button.setFont(QFont("Arial", 36, QFont.Bold))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    color: #333333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            button.clicked.connect(lambda _, i=i: self.make_move(i))
            layout.addWidget(button, (i // 3) + 1, i % 3)
            self.buttons.append(button)

        self.reset_button = QPushButton("Lojë e Re", self)
        self.reset_button.setFont(QFont("Arial", 14))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #333333;
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        self.reset_button.clicked.connect(self.reset_game)
        layout.addWidget(self.reset_button, 4, 0, 1, 3)

    def make_move(self, position):
        """
        Dërgon lëvizjen te serveri.
        """
        if self.board[position] == ' ' and not self.game_over:
            self.client_socket.send(str(position).encode())
            self.board[position] = self.current_player
            self.buttons[position].setText(self.current_player)
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        """
        Kontrollon nëse ka një fitues.
        """
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]              
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.game_over = True
                winner = self.board[combo[0]]
                self.highlight_winner(combo)
                QMessageBox.information(self, "Rezultati", f"Lojtari {winner} fitoi!")
                return
        if ' ' not in self.board:
            self.game_over = True
            QMessageBox.information(self, "Rezultati", "Barazim!")

    def highlight_winner(self, combo):
        """
        Ndryshon ngjyrën e butonave fitues.
        """
        for i in combo:
            self.buttons[i].setStyleSheet("""
                QPushButton {
                    background-color: #d0d0d0;
                    border: 2px solid #b0b0b0;
                    border-radius: 10px;
                    color: #333333;
                }
            """)

    def reset_game(self):
        """
        Rikthen lojën në gjendjen fillestare.
        """
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        for button in self.buttons:
            button.setText(' ')
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    color: #333333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
        self.client_socket.send("reset".encode())

    def receive_updates(self):
        """
        Merr gjendjen e tabelës nga serveri.
        """
        def check_for_updates():
            while True:
                try:
                    data = self.client_socket.recv(1024).decode()
                    if not data:
                        break
                    if data.startswith("Player") or data == "Barazim!":
                        self.game_over = True
                        QMessageBox.information(self, "Rezultati", data)
                    else:
                        self.board = data.split()
                        for i in range(9):
                            self.buttons[i].setText(self.board[i])
                except ConnectionResetError:
                    break
            self.client_socket.close()

        threading.Thread(target=check_for_updates, daemon=True).start()

if __name__ == "__main__":
    app = QApplication([])
    window = TicTacToeGUI()
    window.show()
    app.exec_()