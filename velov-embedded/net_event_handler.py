# -*- coding: utf-8 -*-


"""
Géstionnaire des intérruptions réseau
"""

from event_handler_interface import EventHandlerInterface
from se_states import SystemState


class NetworkEventHandler(EventHandlerInterface):

	def execute(self, args):
		words = args.split()
		if len(words) == 0:
			self._err_msg = "Message réseau reçu vide"
			self._sendAnswer(False)
			return False 
		# On examine les différents cas
		if words[0] == "CHG":
			# Demande de changement d'état du SE
			if len(words) != 5:
				self._err_msg = "Message réseau de changement d'état invalide"
				self._sendAnswer(False)
				return False
			if words[3] not in SystemState.StrToState:
				self._err_msg = "Etat cible inconnu"
				self._sendAnswer(False)
				return False
			if not self._se_state.setState(SystemState.StrToState[words[3]]):
				self._err_msg = "Demande de changement d'état incohérant"
				self._sendAnswer(False)
				return False
		else:
			# Message inconnue
			self._err_msg = "Message réseau inconnu"
			self._sendAnswer(False)
			return False
		# Happy ending
		self._sendAnswer(True)
		return True

	def _sendAnswer(self, ans):
		ans_str = "REP " # "REPly" command
		if (ans):
			ans_str = "OK"
		else:
			ans_str = "NOK"
		ans_str += self._serv_com.getTimestamp() + " " + self._se_state.GetState()
		self._serv_com.sendData(ans_str)
