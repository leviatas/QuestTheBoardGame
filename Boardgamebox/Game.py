import json
from datetime import datetime
from random import shuffle

from Boardgamebox.Player import Player
from Boardgamebox.Board import Board
from Boardgamebox.State import State

class Game(object):
	def __init__(self, cid, initiator):
		self.playerlist = {}
		self.player_sequence = []
		self.cid = cid
		self.board = None
		self.initiator = initiator
		self.dateinitvote = None
		self.history = []
		self.hiddenhistory = []
		self.modulos = []
		self.is_debugging = False
    
    
	def add_player(self, uid, player):
		self.playerlist[uid] = player

	def get_asesino(self):
		for uid in self.playerlist:
			if self.playerlist[uid].rol == "Asesino":
				return self.playerlist[uid]
	def get_goodguys(self):
		resistencia = []
		for uid in self.playerlist:
			if self.playerlist[uid].afiliacion == "Resistencia":
				resistencia.append(self.playerlist[uid])
		return resistencia

	# Lista de espias que se conocen entre ellos
	def get_badguys(self, rol):
		espias = []
		player_number = len(self.playerlist)
		for uid in self.playerlist:
			player = self.playerlist[uid]
			# El changeling no conoce, ni es conocido en ninguna situación
			if (player.afiliacion == "Espia" and not player.rol == "Changeling"):
				# El scion es solo conocido por Morgan Le Fey
				if player.rol == "Scion":
					if rol == "Morgan Le Fey":
						espias.append(player)					
				else:
					# Para juegos de 6 o más el blind hunter no es conocido por sus compañeros
					if player.rol == "Blind Hunter" and player_number >= 6:
						continue
					else:
						espias.append(player)
		return espias

	def get_first_player_loyalty(self):
		# Obtengo la lealtad del primer jugador para el clerigo
		first_player = self.player_sequence[self.board.state.player_counter]
		return first_player.afiliacion

	def get_no_veteranos_no_investigadores_list(self):
		return [player[1] for player in self.playerlist.items() if not player[1].veteran and not player[1].was_investigator]

	def get_veteranos_list(self):
		return [player[1] for player in self.playerlist.items() if player[1].veteran]

	def get_investigadores_list(self):
		return [player[1] for player in self.playerlist.items() if player[1].was_investigator]

	def get_investigados_list(self):
		return [player[1] for player in self.playerlist.items() if player[1].was_investigated]

	def set_veteran(self, uid):
		self.playerlist[uid].veteran = True

	def is_amulet_turn(self):
		# Es -1 porque esto se verifica despues que se puso el resultado de la mision
		turno_actual = len(self.board.state.resultado_misiones)-1
		return "#" in self.board.misiones[turno_actual]

	# (May not choose a Veteran, Investigator, or the new Leader)
	def get_posible_amulet_receiver_players(self):
		return [player[1] for player in self.playerlist.items() if player[1].veteran == False and not player[1].was_investigator]

	def remove_magic_token(self):
		# Se recorre a todos y se quita a todos por si en futuro hay mas de uno o similar.
		for uid in self.playerlist:
			if self.playerlist[uid].has_magic_token:
				self.playerlist[uid].has_magic_token = False

	def set_flag_investigado_e_investigador(sef, investigado, investigador):
		investigado.was_investigated = True
		investigador.was_investigator = True

	def reset_team(self):
		self.board.state.equipo = []
		self.board.state.equipo_contador = 0
		self.board.state.votos_mision = {}
	def shuffle_player_sequence(self):
		for uid in self.playerlist:
			self.player_sequence.append(self.playerlist[uid])
		shuffle(self.player_sequence)

	def remove_from_player_sequence(self, Player):
		for p in self.player_sequence:
			if p.uid == Player.uid:
				p.remove(Player)

	def print_roles(self):
		rtext = ""
		if self.board is None:
			#game was not started yet
			return rtext
		else:
			for p in self.playerlist:
				rtext += "El rol secreto de %s" % (self.playerlist[p].name)
				if self.playerlist[p].esta_muerto:
					rtext += "(muerto) "
				rtext += " era %s (%s)\n" % (self.playerlist[p].rol, self.playerlist[p].afiliacion)
			return rtext

	def encode_all(obj):
		if isinstance(obj, Player):
			return obj.__dict__
		if isinstance(obj, Board):
			return obj.__dict__            
		return obj
    
	def jsonify(self):
		return json.dumps(self.__dict__, default= encode_all)
    
	def get_equipo_actual(self, con_markup):
		miembros_elegidos = ""
		if con_markup:
			for player in self.board.state.equipo:
				miembros_elegidos += "[%s](tg://user?id=%d)\n" % (player.name, player.uid)
		else:
			for player in self.board.state.equipo:
				miembros_elegidos += "%s\n" % (player.name)
		return miembros_elegidos
	
	def get_equipo_actual_flat(self, con_markup):
		miembros_elegidos = ""
		if con_markup:
			for player in self.board.state.equipo:
				miembros_elegidos += "[%s](tg://user?id=%d) " % (player.name, player.uid)
		else:
			for player in self.board.state.equipo:
				miembros_elegidos += "%s - " % (player.name)
		miembros_elegidos = miembros_elegidos[:-3]
		return miembros_elegidos
	
	def get_badguys2(self):
		espias = []
		for uid in self.playerlist:
			if self.playerlist[uid].afiliacion == "Espia" and not self.playerlist[uid].rol == "Encubierto": 
				espias.append(self.playerlist[uid])
		return espias
	
	def get_comandantes(self):
		espias = []
		for uid in self.playerlist:
			if self.playerlist[uid].rol in ("Comandante", "Comandante Falso"): 
				espias.append(self.playerlist[uid])
		return espias
	
	def jugador_con_carta(self, nombre_carta):
		result = False
		for uid in self.playerlist:
			if nombre_carta in self.playerlist[uid].cartas_trama:
				return True
		return result
	
	def get_creadores_de_opinion(self):
		creador_de_opinion = []
		for uid in self.playerlist:
			if self.playerlist[uid].creador_de_opinion:
				creador_de_opinion.append(self.playerlist[uid])
		return creador_de_opinion
	
	def get_jefes_resistencia(self):
		jefes = []
		for uid in self.playerlist:
			if self.playerlist[uid].rol in ("Jefe Resistencia", "Jefe Resistencia 2"): 
				jefes.append(self.playerlist[uid])
		return jefes
	
	def get_coordinador(self):
		coordinador = []
		for uid in self.playerlist:
			if self.playerlist[uid].rol == "Coordinador": 
				coordinador.append(self.playerlist[uid])
		return coordinador
	
	def get_cazador_resistencia(self):
		for uid in self.playerlist:
			if self.playerlist[uid].rol == "Cazador Resistencia":
				return self.playerlist[uid]
			
	def get_cazador_espia(self):
		for uid in self.playerlist:
			if self.playerlist[uid].rol == "Cazador Espia":
				return self.playerlist[uid]

	
	
