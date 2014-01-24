# -*- coding: utf-8 -*-


"""
Géstionnaire des interruptions provenant du boutton
"""

from event_handler_interface import EventHandlerInterface
from se_states import SystemState


class ButtonEventHandler(EventHandlerInterface):
	
	def execute(self, args):
		if self._se_state.GetState() != SystemState.Unlockable:
			self._err_msg = "Le vélo n'est pas dévérouillable"
			self._serv_com.sendStatusChg(self._se_state.GetState())
			return False
		if self._serv_com.sendStatusChg(SystemState.Used):
			self._se_state.setState(SystemState.Used)
			return True
		self._err_msg = "On n'a pas pu prévenir le PC"
		return False
