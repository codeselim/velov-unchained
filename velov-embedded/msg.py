# -*- coding: utf-8 -*-

"""
Définit les message échangé entre les deux threads
"""

class MsgType(object):
	'''
	Enumeration représentant le type de message échangé.
	Chaque type de message peut-être assimilé à une ligne d'interruption
	'''
	Quit = 'Quit'
	Locker = 'Locker'
	Button = 'Button'
	Net = 'Net'
	GpsLoc = 'GpsLoc'


class Msg(object):
	"""Classe représentant un message de la FIFO"""

	def __init__(self, msg_type, data):
		"""
		Initialisation.
		msg_type: objet de type FIFO_Msg pour indiquer le type du message
		data: données supplémentaire pour le message, ou null.
		"""
		self.type = msg_type
		self.data = data

class MsgWithSocket(Msg):
	"""Msg... with socket"""
	def __init__(self, msg_type, data, socket):
		super(MsgWithSocket, self).__init__(msg_type, data)
		self.socket = socket
		