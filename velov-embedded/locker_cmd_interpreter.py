# -*- coding: utf-8 -*-

"""
Interprette la commande du locker
"""

from cmd_interpreter_interface import CmdInterpreterInterface
from msg import Msg, MsgType


class LockerCmdInterpreter(CmdInterpreterInterface):
	"""
	Format de la commande:
	l
	"""

	def buildMsg(self, words):
		"""
		"""
		if len(words) != 1:
			return None
		if words[0] == "l":
			return Msg(MsgType.Locker, None)
		return None
