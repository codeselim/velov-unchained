# -*- coding: utf-8 -*-


"""
Géstionnaire des interruptions pour une demande d'envoie GPS
"""

from event_handler_interface import EventHandlerInterface


class GpsEventHandler(EventHandlerInterface):
	
	def execute(self, args):
		self._serv_com.sendGpsLoc()
		return True
