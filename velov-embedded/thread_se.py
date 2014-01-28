# -*- coding: utf-8 -*-

"""
Thread du système embarquée.
Le SE réagit aux interruptions qui sont ici simulées par des messages FIFO.
Lorsqu'une interruption est reçue, le SE la traite en appelant le handler
correspondant.
Les interruptions sont traitées les unes à la suite des autres. Elles ne sont pas
imbriquées ou prioritisées.
"""


from thread_base import ThreadBase
from fifo_itc import FifoITC
from net_event_handler import NetworkEventHandler
from button_event_handler import ButtonEventHandler
from locker_event_handler import LockerEventHandler
from gps_event_handler import GpsEventHandler
from msg import MsgType, Msg
from se_states import SystemState
from net_com_to_server_module import NetComToServerModule
from bat_event_handler import BatteryEventHandler


class ThreadSE(ThreadBase):
	"""Thread du système embarqué"""

	def __init__(self, title, fifo, nlines, ncols, begin_y, begin_x, window_lock):
		"""
		Initialisation
		"""
		# Initialisation du parent
		ThreadBase.__init__(self, title, fifo, nlines, ncols, begin_y, begin_x, window_lock)		
		# Moyen de com avec le serveur
		self._serv_com = NetComToServerModule(self._writeLineOnScreen)
		# État du système
		self._state = SystemState(SystemState.Available, self._writeLineOnScreen, self._cleanScreen, self._serv_com)
		# Dictionnaire qui associe à chaque type de message un event handler
		self._handlers = {}
		self._handlers[MsgType.Net] = NetworkEventHandler(self._state,self._serv_com)
		self._handlers[MsgType.Button] = ButtonEventHandler(self._state, self._serv_com)
		self._handlers[MsgType.Locker] = LockerEventHandler(self._state, self._serv_com)
		self._handlers[MsgType.GpsLoc] = GpsEventHandler(self._state, self._serv_com)
		self._handlers[MsgType.Battery] = BatteryEventHandler(self._state, self._serv_com)


	def run(self):
		"""
		Réagit aux interruptions, qui sont simulées par des messages FIFO
		"""
		while True:
			# On bloque en attendant une it
			msg = self._itc_fifo.GetMsg()
			# On traite le message
			if msg.type == MsgType.Quit:
				self._state.stopAllTimers()
				break
			else:
			 	if msg.type in self._handlers:
			 		handler = self._handlers[msg.type]
			 		if not handler.execute(msg):
			 			self._writeLineOnScreen("/!\ Erreur à l'exec du handler:")
			 			self._writeLineOnScreen(handler._err_msg)
			 	else:
			 		self._writeLineOnScreen("Handler introuvable: " + msg.type)
	
	def _initScreen(self):
		"""
		Initialise la fenêtre d'affichage
		"""
		self._body_win.clear()
		# Bordure des fenêtres
		self._body_win.border(0, 1, 1, 1, 0, 1, 0, 1)
		# On met à jour
		self._body_win.refresh()
