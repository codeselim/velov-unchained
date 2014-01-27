# -*- coding: utf-8 -*-


"""
Module du GPS
"""


from threading import Timer


# Privée
_MOVE_TIME = 10
_timer = None
_dx = None
_dy = None
_current_time_step = None
_gps_current_pos = [0.0, 0.0]	# Lat, Long


def getCurrentPos():
	return _gps_current_pos

def moveBike(to_lat, to_long):
	global _timer, _dx, _dy, _current_time_step, _gps_current_pos, _MOVE_TIME
	_dx = (to_lat - _gps_current_pos[0]) / float(_MOVE_TIME)
	_dy = (to_long - _gps_current_pos[1]) / float(_MOVE_TIME)
	_current_time_step = 0
	_timer = Timer(1.0, _move_cb)
	_timer.start()

def stopMovingBike():
	global _timer
	if _timer is not None:
		_timer.cancel()
		_timer = None

def _move_cb():
	global _timer, _dx, _dy, _current_time_step, _gps_current_pos, _MOVE_TIME
	_timer = None
	_gps_current_pos[0] += _dx
	_gps_current_pos[1] += _dy
	_current_time_step += 1
	if (_current_time_step < _MOVE_TIME):
		_timer = Timer(1.0, _move_cb)
		_timer.start()
