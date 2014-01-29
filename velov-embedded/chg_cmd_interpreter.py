# -*- coding: utf-8 -*-

"""
Interprette la commande de changement d'état
"""

from cmd_interpreter_interface import CmdInterpreterInterface
from msg import Msg, MsgType


class ChgCmdInterpreter(CmdInterpreterInterface):
	"""
	Format de la commande:
	chg <etat>
	"""

	def buildMsg(self, words):
		"""
		"""
		if len(words) != 2:
			return None
		if words[0] == "chg":
			return Msg(MsgType.State, words[1])
		return None
