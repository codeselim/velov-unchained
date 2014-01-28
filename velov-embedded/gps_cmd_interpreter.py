# -*- coding: utf-8 -*-

"""
Interprette la commande du GPS
"""

from cmd_interpreter_interface import CmdInterpreterInterface
from msg import Msg, MsgType


class GpsCmdInterpreter(CmdInterpreterInterface):
	"""
	Format de la commande:
	l
	"""

	def buildMsg(self, words):
		"""
		"""
		if len(words) != 1:
			return None
		if words[0] == "gl":
			return Msg(MsgType.GpsLoc, None)
		return None
