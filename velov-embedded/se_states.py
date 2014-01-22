# -*- coding: utf-8 -*-

"""
États du système embarqué
"""

from threading import Timer


# Délai pendant lequel le vélo reste débloquable.
# C'est le temps qu'à l'utilisateur pour le récupérer
UNLOCKABLE_DELAY	=	30.0 # En secondes


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
				Stolen 		: (Available, Unusable, Reserved, Unlockable),
				Unusable 	: (Available, Off),
				Reserved	: (Available),
				Unlockable	: (Reserved, Available),
				Available	: (Reserved, Unlockable, Used, Unusable, Off),
				Off 		: (Unusable, Available),
				Unknown		: (Used, Stolen, Unusable, Reserved, Unlockable, Available, Off)
	}

	def __init__(self, default_state, print_func, clean_func):
		"""
		Initialisation
		"""
		self._state = default_state
		self._print_func = print_func
		self._clean_func = clean_func
		self._timer = None

	def setState(self, new_state):
		"""
		Change l'état du vélo
		"""
		if self._state not in SystemState.Sources[new_state]:
			return False
		
		self._state = new_state
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

	def _unlockable_trigger(self):
		"""
		Trigger appelé lorsque le vélo devient délockable
		"""
		self._timer = Timer(UNLOCKABLE_DELAY, self._relock)
		self._timer.start()
		self._show_state()

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
		self._timer.cancel()
		self._show_state()

	# Triggers
	# Méthode à appeler lorsque l'on entre dans un état
	Triggers = {	Used		: _used_trigger,
					Stolen 		: _show_state,
					Unusable 	: _show_state,
					Reserved	: _show_state,
					Unlockable	: _unlockable_trigger,
					Available	: _show_state,
					Off 		: _show_state,
					Unknown		: _show_state
	}
