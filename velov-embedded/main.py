# -*- coding: utf-8 -*- 

"""
Main
"""


import threading
import curses
import random


from fifo_itc import FifoITC
from thread_sim import ThreadSim
from thread_se import ThreadSE


if __name__ == "__main__":
	#
	# Initialisation du RND
	random.seed()

	#
	# Initialisation de Curses et du screen
	stdscr = curses.initscr()
	curses.nocbreak()

	# Fifo pour la communication entre les threads
	thread_fifo = FifoITC()

	# Lock pour l'écriture sur le screen
	win_lock = threading.Lock()

	# Création du thread simulateur
	thread_sim = ThreadSim("Simulateur",
		thread_fifo,
		curses.LINES, curses.COLS / 2, 0, 0,
		win_lock)

	# Création du thread ThreadSE
	thread_se = ThreadSE("Système embarqué",
		thread_fifo,
		curses.LINES, curses.COLS / 2, 0, curses.COLS / 2,
		win_lock)

	# On lance les Thread
	thread_sim.start()
	thread_se.start()

	# On attend la fin
	thread_sim.join()
	thread_se.join()
	# On nettoie
	curses.endwin()
