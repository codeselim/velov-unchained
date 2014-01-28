# -*- coding: utf-8 -*-

"""
Interprette la commande pour dire que la batterie est vide
"""

from cmd_interpreter_interface import CmdInterpreterInterface
from msg import Msg, MsgType


class BatteryCmdInterpreter(CmdInterpreterInterface):
	"""
	Format de la commande:
	be
	"""

	def buildMsg(self, words):
		"""
		"""
		if len(words) != 1:
			return None
		if words[0] == "be":
			return Msg(MsgType.Battery, None)
		return None
