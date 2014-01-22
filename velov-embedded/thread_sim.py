# -*- coding: utf-8 -*-

"""
Thread du simulateur.
Ce thread est chargé de:
- Recevoir du texte depuis l'entrée standard
- Analyser le texte
- Envoyer le message (interruption) correspondant au thread qui simule le
système embarqué
"""


from curses import ascii
from threading import Thread
from SocketServer import TCPServer, BaseRequestHandler

from thread_base import ThreadBase
from fifo_itc import FifoITC
from msg import Msg, MsgType, MsgWithSocket
from cmd_interpreter_interface import CmdInterpreterInterface
from button_cmd_interpreter import ButtonCmdInterpreter

SERVER_PORT = 5000
SERVER_HOST = "localhost"


class NetworkServerHandler(BaseRequestHandler):

	fifo = None

	def handle(self):
		# Construction du message pour la FIFO
		# Reads until we find "\n"
		total_data=[];data=''
		end = "\n"
		while True:
			data=self.request.recv(8192)
			if end in data:
				total_data.append(data[:data.find(end)])
				break
				total_data.append(data)
				if len(total_data)>1:
					#check if end_of_data was split
					last_pair=total_data[-2]+total_data[-1]
					if end in last_pair:
						total_data[-2]=last_pair[:last_pair.find(End)]
						total_data.pop()
						break
		data = ''.join(total_data)
		msg = MsgWithSocket(MsgType.Net, data.strip(), self.request)
		# Envoi du message
		NetworkServerHandler.fifo.AddMsg(msg)

class MyTCPServer(TCPServer, object):
	def __init__(self, address, request_handler, reuse_address=False):
		self.allow_reuse_address = reuse_address
		super(MyTCPServer, self).__init__(address, request_handler)		
	
	def process_request(self, request, client_address):
		"""
		Overriding BaseServer default behaviour of shutting down the request
		at the end of request processing by letting the request
		be shut down from somewhere else
		"""
		super(MyTCPServer, self).finish_request(request, client_address)
		# self.shutdown_request(request)

class NetworkServerThread(Thread):

	def __init__(self, port, host, handler):
		Thread.__init__(self)
		self._server = MyTCPServer((host, port), handler, reuse_address=True)

	def run(self):
		self._server.serve_forever()

	def shutdown(self):
		self._server.shutdown()


class ThreadSim(ThreadBase):
	"""Thread du simulateur"""

	def __init__(self, title, fifo, nlines, ncols, begin_y, begin_x, window_lock):
		"""
		Initialisation
		"""
		# Initialisation du parent
		ThreadBase.__init__(self, title, fifo, nlines, ncols, begin_y, begin_x, window_lock)
		# Dictionnaire contenant les interpréteur
		self._interpreters = {}
		self._interpreters["b"] = ButtonCmdInterpreter()
		# On met en place le serveur réseau
		NetworkServerHandler.fifo = fifo
		self._server_thread = NetworkServerThread(SERVER_PORT, SERVER_HOST, NetworkServerHandler)

	def run(self):
		"""
		Lit l'entrée de l'utilisateur
		"""
		# On lance le thread serveur
		self._server_thread.start()
		# On surveille STDIN
		while True:
			self._writeLineOnScreen(">> ")
			# On lit l'entrée
			inp = ""
			ch = self._body_win.getch()
			while ch != ascii.NL:
				inp += ascii.unctrl(ch)
				ch = self._body_win.getch()
			# On construit puis on envoie le message au thread SE
			msg = self._build_msg(inp)
			self._send_msg(msg)
			# Si l'utilisateur veut quitter...
			if inp == "quit":
				# On ferme le serveur
				self._server_thread.shutdown()
				self._server_thread.join()
				# Et voilà...
				break

	def _build_msg(self, raw_str_input):
		"""
		Analyse l'entrée de l'utilisateur puis envoye le message.
		raw_input: Entrée brute de l'utilisateur sous forme de chaine de caractère
		renvoie le message
		"""
		msg = None
		words = raw_str_input.split()
		if len(words) == 0:
			return
		if words[0] == "quit":
			# Cas ou l'utilisateur veut quitter l'application
			msg = Msg(MsgType.Quit, None)
		else:
			if words[0] in self._interpreters:
				msg = self._interpreters[words[0]].buildMsg(words)
			else:
				self._writeLineOnScreen("Commande inconnue.")
		return msg

	def _send_msg(self, msg):
		"""
		Envoye le message au thread SE
		msg: message a envoyer
		"""
		if msg != None:
			self._itc_fifo.AddMsg(msg)
