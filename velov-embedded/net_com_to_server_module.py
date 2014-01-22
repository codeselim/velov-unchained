# -*- coding: utf-8 -*-


"""
Communication avec le serveur
"""


import socket
import time
import random

NET_HOST	=	"localhost"
NET_PORT	=	3000


class NetComToServerModule:
	"""
	Permet de communiquer avec le serveur
	"""

	def __init__(self, print_func):
		# On génère aléatoirement l'ID du vélo
		self._id = random.randint(0, 1000000)
		# Fonction pour afficher des messages
		self._print_func = print_func
		# Socket pour répondre au serveur
		try:
			self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._socket.connect((NET_HOST, NET_PORT))
		except:
			self._print_func("Echec de la connextion au serveur")

	def close(self):
		self._socket.close()

	def sendData(self, data):
		try:
			self._socket.sendall(data + "\t" + "foo_checksum" + "\n")
		except:
			self._print_func("Echec de l'envoie du msg au serveur")

	def getTimestamp(self):
		return str(time.time())

	def getID(self):
		return self._id

	def sendStatusChg(self, current_status):
		data = "CHG " + str(self._id) + " " + self.getTimestamp() + " " + current_status
		self.sendData(data)
