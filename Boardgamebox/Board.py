from Constants.Cards import playerSets
from Constants.Cards import modules
import random
from Boardgamebox.State import State

class Board(object):
    def __init__(self, playercount, game):
        self.state = State()
        self.num_players = playercount
        self.misiones = playerSets[self.num_players]["misiones"]            
        self.discards = []
        self.previous = []
    def print_board(self, player_sequence):
        board = "--- Misiones ---\n"
        
        for i in range(5):
            # Pongo la cantidad de miembros por mision como primera fila
            # pongo un espacio extra luego de 4 porque esta el * de mision en casod e mas de 6 jugadores
            if i == 3 and self.num_players > 6:
                board += "  " + str(i+1) + "      "
            elif i == 4 and self.num_players > 6:
                board += "   " + str(i+1) + "      "
            else:        
                board += " " + str(i+1) + "     "            
            
        board += "\n"
        
        for i in range(5):
            # Pongo la cantidad de miembros por mision como primera fila
            board += " " + self.misiones[i].replace('*', '\*') + "     " #X
        board += "\n"
        
        # Seguimiento de misiones
        
        for resultado in self.state.resultado_misiones :
            if resultado == "Exito":
                board += u"\u2714\uFE0F" + " " #dove
            else:
                board += u"\u2716\uFE0F" + "  " #X
        
        board += "\nGuía\n\* Mision que requiere dos fallos\n\# Mision que cuando termina se asigna amuleto de investigación\n"
        board += "\n--- Orden de turno  ---\n"
        
        for player in player_sequence:
            if self.state.lider_actual == player:
                board += "*" + player.name + "*" + " " + u"\u27A1\uFE0F" + " "
            else:
                board += player.name + " " + u"\u27A1\uFE0F" + " "
        board = board[:-1]
        board += u"\U0001F501"        
        return board