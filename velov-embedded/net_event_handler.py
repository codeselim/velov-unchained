# -*- coding: utf-8 -*-


"""
Géstionnaire des intérruptions réseau
"""

from event_handler_interface import EventHandlerInterface
from se_states import SystemState
from socket import SHUT_RDWR

class NetworkEventHandler(EventHandlerInterface):

	def execute(self, server_msg):
		args = server_msg.data
		words = args.split()
		if len(words) == 0:
			self._err_msg = "Message réseau reçu vide"
			self._sendAnswer(False)
			return False 
		# On examine les différents cas
		if words[0] == "CHG":
			# On reprend l'ID
			self._serv_com.setID(int(words[1]))
			# Demande de changement d'état du SE
			if len(words) != 5:
				self._err_msg = "Message réseau de changement d'état invalide"
				self._sendAnswer(server_msg, False)
				return False
			if words[3] not in SystemState.StrToState:
				self._err_msg = "Etat cible inconnu"
				self._sendAnswer(server_msg, False)
				return False
			if not self._se_state.setState(SystemState.StrToState[words[3]]):
				self._err_msg = "Demande de changement d'état incohérant"
				self._sendAnswer(server_msg, False)
				return False
		else:
			# Message inconnue
			self._err_msg = "Message réseau inconnu"
			return False
		# Happy ending
		self._sendAnswer(server_msg, True)
		return True

	def _sendAnswer(self, server_msg, ans):
		ans_str = "REP "
		if (ans):
			ans_str += "OK "
		else:
			ans_str += "NOK "
		ans_str += self._serv_com.getTimestamp() + " " + self._se_state.GetState()
		frame = self._serv_com.buildFrame(ans_str)
		server_msg.socket.sendall(frame)
		server_msg.socket.shutdown(SHUT_RDWR) # Necessary to actually close the connection, close() waits for GC to close
		server_msg.socket.close()
