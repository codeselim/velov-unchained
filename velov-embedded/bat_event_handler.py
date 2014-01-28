# -*- coding: utf-8 -*-


"""
Géstionnaire des interruptions provenant d'une batterie vide
"""

from event_handler_interface import EventHandlerInterface
from se_states import SystemState


class BatteryEventHandler(EventHandlerInterface):
	
	def execute(self, args):
		# On prévient que la batterie est quasi vide
		self._serv_com.empBatMsg()
		return True
