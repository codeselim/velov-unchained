# -*- coding: utf-8 -*- 

"""FIFO pour la communication entre les thread"""


import threading
import collections


class FifoITC:
	"""
	Permet l'échange de message en FIFO entre le simulateur est le prototype
	de SE
	"""

	def __init__(self):
		"""	Initialisation"""
		self._fifo = collections.deque()
		self._synch_cond = threading.Condition()

	def AddMsg(self, new_msg):
		"""
		Ajoute un message à la FIFO
		new_msg: message à ajouter, qui doit-être de type FIFO_Msg
		"""
		with self._synch_cond: # Récupère le lock pour la durée du block sous-jacent
			self._fifo.append(new_msg)
			self._synch_cond.notify()
		# Ici, le lock est libérée automatiquement par le with

	def GetMsg(self):
		"""
		Retourne le plus vieux message.
		Si la FIFO ne contient pas de message, block jusqu'a se qu'il y en ai un.
		"""
		msg = None
		with self._synch_cond:	# Récupère le lock
			while len(self._fifo) == 0:
				self._synch_cond.wait()	# Libère le lock est attend un notify
			# Là, on a le lock est la queue n'est pas vide
			msg = self._fifo.popleft()
		# Le lock est libéré par le with
		return msg
