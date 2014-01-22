# -*- coding: utf-8 -*-

"""
Interprette la commande de boutton
"""

from cmd_interpreter_interface import CmdInterpreterInterface
from msg import Msg, MsgType


class ButtonCmdInterpreter(CmdInterpreterInterface):
	"""
	Format de la commande:
	b
	"""

	def buildMsg(self, words):
		"""
		"""
		if len(words) != 1:
			return None
		if words[0] == "b":
			return Msg(MsgType.Button, None)
		return None
