# -*- coding: utf-8 -*-


"""
Géstionnaire des interruptions provenant du boutton
"""

from event_handler_interface import EventHandlerInterface
from se_states import SystemState


class LockerEventHandler(EventHandlerInterface):
	
	def execute(self, args):
		if self._se_state.GetState() != SystemState.Used:
			self._err_msg = "Le vélo n'est pas utilisé"
			return False
		# On demande l'authorisation au vélo
		if self._serv_com.reqLockAth():
			self._se_state.setState(SystemState.Available)
			self._serv_com.sendStatusChg(SystemState.Available)
			return True
		self._err_msg = "On n'a pas eu l'authrisation du serveur"
		return False
