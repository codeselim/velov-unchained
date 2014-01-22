# -*- coding: utf-8 -*-

"""
Classe de base pour les threads du programme.
Fournit des fonctionnalités communes pour:
- Écrire du texte du la fenêtre
- La communication par FIFO thread-safe
"""


import threading
import curses


class ThreadBase(threading.Thread):
	"""Classe de base pour les threads de l'application"""

	def __init__(self, title, fifo, nlines, ncols, begin_y, begin_x, window_lock):
		"""
		Initialisation.
		title: nom du thread. Sera dans l'en-tête de la fenêtre
		fifo: ITC Fifo utilisé pour la communication
		nlines: nombre de lignes de la fenêtre
		ncols: nombre de colones de la fenêtre
		begin_y/begin_x: début de la fenêtre
		window_lock: Lock ITC utilisé pour synchroniser les écriture Curses
		"""
		threading.Thread.__init__(self)
		self._itc_fifo = fifo
		# Fenêtre header : création et initialisation
		self._header_win = curses.newwin(3, ncols, begin_y, begin_x)
		self._header_win.border(0, 0, 0, 0, 0, 0, 0, 0)
		self._header_win.addstr(1, (ncols - len(title)) / 2, title)
		self._header_win.refresh()
		# Fenetre corps : création
		self._body_win = curses.newwin(nlines - 3, ncols,
			begin_y + 3, begin_x)
		# Lock pour l'accès aux fenêtre
		self._lock_body_win = window_lock
		# Numéro de la ligne actuelle à laquelle écrire
		self._line_number = 0
		# Initialise la fenêtre corps
		self._initScreen()

	def _cleanScreen(self):
		self._initScreen()
		self._line_number = 0

	def _writeLineOnScreen(self, text):
		"""
		Écrit sur la fenetre
		text: texte à écrire
		"""
		if self._lock_body_win.acquire():
			# Si l'écran est plein, on le nettoie
			if self._line_number == (self._body_win.getmaxyx()[0] - 1):
				self._cleanScreen()
			self._body_win.addstr(self._line_number, 2, text)
			self._body_win.refresh()
			self._lock_body_win.release()
			self._line_number += 1

	def _initScreen(self):
		"""
		Initialise la fenêtre d'affichage
		"""
		self._body_win.clear()
		self._body_win.refresh()

