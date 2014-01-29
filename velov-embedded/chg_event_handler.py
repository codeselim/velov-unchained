# -*- coding: utf-8 -*-


"""
Géstionnaire des intérruptions réseau
"""

from event_handler_interface import EventHandlerInterface
from se_states import SystemState
from socket import SHUT_RDWR

class ChgEventHandler(EventHandlerInterface):

	def execute(self, server_msg):
		new_state_str = server_msg.data
		# Demande de changement d'état du SE
		if new_state_str not in SystemState.StrToState:
			self._err_msg = "Etat cible inconnu"
			return False
		if not self._se_state.setState(SystemState.StrToState[new_state_str]):
			self._err_msg = "Demande de changement d'état incohérant"
			return False
		# Happy ending
		self._serv_com.sendStatusChg(self._se_state.GetState())
		return True
