# -*- coding: utf-8 -*-

"""
États du système embarqué
"""

from threading import Timer
import time
import gps_module


# Délai pendant lequel le vélo reste débloquable.
# C'est le temps qu'à l'utilisateur pour le récupérer
UNLOCKABLE_DELAY	=	30.0		# En secondes
RESERVED_DELAY		= 	(5.*60.)	# En secondes
#
STLN_TIMES			=	(	5.*60.,
							20.*60.,
						)
STLN_DELAYS			=	(	60.0,	# Les 5 premières minutes
							5.*60., # Les 15 minutes ensuites
							3.*60.) # Ensuite


class SystemState:
	"""
	Différents états que peut prendre un vélo
	"""

	Unknown		= "UKN"	# État inconnu
	Used		= "USE"	# Vélo en cours d'utilisation
	Stolen		= "STO"	# Vélo volé
	Unusable	= "UNU"	# Vélo inutilisable (maintenance,...), mais toujours dans la nature
	Reserved	= "RES"	# Vélo réservé
	Unlockable	= "UNL"	# Vélo dévérouiable
	Available 	= "AVA"	# Disponible mais ni utilisé, ni réservé
	Off			= "OFF"	# Vélo entre les mains du service maintenance

	# Permet de passer d'une chaine à un état
	StrToState = {	"UKN"	: Unknown,
					"USE"	: Used,
					"STO"	: Stolen,
					"UNU"	: Unusable,
					"RES"	: Reserved,
					"UNL"	: Unlockable,
					"AVA"	: Available,
					"OFF"	: Off
	}

	# Associe à chaque état les états sources possible
	Sources = { Used 		: (Unlockable),
				Stolen 		: (Available, Unusable, Reserved, Unlockable, Stolen),
				Unusable 	: (Available, Off),
				Reserved	: (Available),
				Unlockable	: (Reserved, Available),
				Available	: (Reserved, Unlockable, Used, Unusable, Off),
				Off 		: (Unusable, Available),
				Unknown		: (Used, Stolen, Unusable, Reserved, Unlockable, Available, Off)
	}

	def __init__(self, default_state, print_func, clean_func, serv_com):
		"""
		Initialisation
		"""
		self._state = None
		self._print_func = print_func
		self._clean_func = clean_func
		self._timer = None
		self._stln_timer = None
		self._serv_com = serv_com
		self._locked_time = None
		self._prev_pos = []
		for c in gps_module.getCurrentPos():
			self._prev_pos.append(c)
		self.setState(default_state)

	def setState(self, new_state):
		"""
		Change l'état du vélo
		"""
		if (self._state is not None) and (self._state not in SystemState.Sources[new_state]):
			return False
		
		# On détermine si le système est nouvellement vérouillé
		new_lock = False
		if self._state == None:
			new_lock = True
		elif self._state == SystemState.Used or self._state == SystemState.Off:
			if new_state != SystemState.Used and new_state != SystemState.Off:
				new_lock = True
		# On change l'état
		self._state = new_state
		# On lance le système anti-vol
		if new_lock:
			self._locked_time = time.time()
			self._stln_start()
		elif new_state == SystemState.Used or new_state == SystemState.Off:
			self._stln_stop()
		# Si il y a des triggers associés à ce vélo, on les appellent
		if new_state in SystemState.Triggers:
			SystemState.Triggers[new_state](self)
		return True

	def GetState(self):
		"""
		Renvoie l'état du vélo
		"""
		return self._state

	#
	# Concerne l'état où le vélo est débloquable.
	# Le vélo ne peut pas rester longtemps débloquable, sinon on pourrait le vélo

	def _relock(self):
		self.setState(SystemState.Available)
		self._serv_com.sendStatusChg(self._state)

	def _unlockable_trigger(self):
		"""
		Trigger appelé lorsque le vélo devient délockable
		"""
		self._timer = Timer(UNLOCKABLE_DELAY, self._relock)
		self._timer.start()

	def _show_state(self):
		"""
		Affiche l'état courant du vélo.
		Simule les LED
		"""
		self._clean_func()
		led_st = None
		self._print_func("Etat actuel : %s" % self._state)
		# LED verte
		if self._state == SystemState.Available:
			led_st = "allumé"
		elif self._state == SystemState.Unlockable:
			led_st = "clignote"
		else:
			led_st = "éteinte"
		self._print_func("-- LED Verte : %s" % led_st)
		# LED Rouge
		if self._state == SystemState.Used:
			led_st = "allumé"
		elif self._state == SystemState.Unusable:
			led_st = "clignote"
		else:
			led_st = "éteinte"
		self._print_func("-- LED Rouge : %s" % led_st)
		# LED jaune
		if self._state == SystemState.Reserved:
			led_st = "allumé"
		else:
			led_st = "éteinte"
		self._print_func("-- LED Jaune : %s" % led_st)

	#
	# Trigger pour le passage en mode Used
	def _used_trigger(self):
		if self._timer is not None:
			self._timer.cancel()
			self._timer = None

	#
	# Trigger pour l'état réservé
	def _reserved_trigger(self):
		self._timer = Timer(RESERVED_DELAY, self._relock)
		self._timer.start()

	#
	# Check le vole
	def _stln_start(self):
		# Vérifier si le vélo à bougé
		move = self._updateCurrentPos()
		if move:
			self.setState(SystemState.Stolen)
		# On remet le timer
		i = 0
		found = False
		while i < len(STLN_TIMES):
			if time.time() - self._locked_time < STLN_TIMES[i]:
				self._stln_timer = Timer(STLN_DELAYS[i], self._stln_start)
				self._stln_timer.start()
				found = True
				break
			i += 1
		if not found:
			self._stln_timer = Timer(STLN_DELAYS[-1], self._stln_start)
			self._stln_timer.start()

	def _stln_stop(self):
		if self._stln_timer is not None:
			self._stln_timer.cancel()
			self._stln_timer = None

	def _stln_trigger(self):
		self._clean_func()
		self._show_state()
		self._serv_com.sendStlnMsg()

	def _updateCurrentPos(self):
		i = 0
		move = False
		for c in gps_module.getCurrentPos():
			if c != self._prev_pos[i]:
				move = True
			self._prev_pos[i] = c
			i += 1
		return move

	def stopAllTimers(self):
		if self._timer is not None:
			self._timer.cancel()
			self._timer = None
		if self._stln_timer is not None:
			self._stln_timer.cancel()
			self._stln_timer = None

	# Triggers
	# Méthode à appeler lorsque l'on entre dans un état
	Triggers = {	Used		: _used_trigger,
					Stolen 		: _stln_trigger,
					Reserved	: _reserved_trigger,
					Unlockable	: _unlockable_trigger,
	}

