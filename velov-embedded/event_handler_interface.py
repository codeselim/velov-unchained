# -*- coding: utf-8 -*-

"""
Interface utilisée pour implémenter une opération réalisée
par le SE en réaction à un évènement (interruption, évènement...)
C'est un Event Handler.
"""

class EventHandlerInterface:

	def __init__(self, state, serv_com):
		"""
		Initialisation.
		state: état à modifier
		"""

		self._se_state = state
		# Dernier message d'erreur
		self._err_msg = None
		# Com avec le serveur
		self._serv_com = serv_com
	
	def execute(self, args):
		"""
		Execute le handler event
		Fonction à overloader par les différents handler events.
		"""
		pass
