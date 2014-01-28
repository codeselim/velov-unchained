# -*- coding: utf-8 -*-


"""
Communication avec le serveur
"""


import socket
import time
import random
from gps_module import getCurrentPos

NET_HOST	=	"localhost"
NET_PORT	=	3000


class NetComToServerModule:
	"""
	Permet de communiquer avec le serveur
	"""

	def __init__(self, print_func):
		# On génère aléatoirement l'ID du vélo
		self._id = 1
		# Fonction pour afficher des messages
		self._print_func = print_func

	def sendData(self, data):
		try:
			self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._socket.connect((NET_HOST, NET_PORT))
			self._socket.sendall(data + "\t" + "foo_checksum" + "\n")
			self._socket.close()
			return True
		except:
			self._print_func("Echec de l'envoie du msg au serveur")
			return False

	def getTimestamp(self):
		return str(int(time.time()))

	def getID(self):
		return self._id

	def sendStatusChg(self, current_status):
		data = "CHG " + str(self._id) + " " + self.getTimestamp() + " " + current_status
		return self.sendData(data)

	def reqLockAth(self):
		try:
			self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._socket.connect((NET_HOST, NET_PORT))
			self._socket.sendall("CHG " + str(self.getID()) + " " + self.getTimestamp() + " RLK" + "\t" + "foo_checksum" + "\n")
			ans = self._socket.recv(4096)
			ans_words = ans.split()
			self._socket.close()
			if len(ans_words) > 2:
				if ans_words[1] == "OK":
					return True
			return False
		except Exception as e:
			self._print_func("Echec de la demande de délocking au serveur %s" % str(e))
			return False

	def sendGpsLoc(self):
		self.sendData("LOC " + str(self.getID()) + " " + self.getTimestamp() + " " + str(getCurrentPos()[0]) + " " + str(getCurrentPos()[1]))

	def sendStlnMsg(self):
		self.sendData("STL " + str(self.getID()) + " " + self.getTimestamp() + " " + str(getCurrentPos()[0]) + " " + str(getCurrentPos()[1]))
