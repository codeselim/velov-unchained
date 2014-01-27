"use strict"

var pgsql = require('./pgsql')

var TABLE_NAMES = { // shortens the code, and avoids spelldraws, in short, THIS IS [SPARTA?] CONSTANTS!
	  'loc_histo': "velov_location_history"
	, 't': "velov_tasks"
	, 'tt': "task_types"
	, 'sh': "velov_state_history"
	, 's': "states"
	, 'uah': "user_action_history"
	, 'urs': "user_renting_sessions"
	, 'fz': "zones_interdites"
}

var TASK_STATES_CODES = {
	  'todo': 1
	, 'inprogress': 2
	, 'success': 3
	, 'failure': 4
}

// Yeah, should be loaded dynamically from db, will surely do that once we've got time... !
var USER_ACTION_CODES = {
	  'ask_unlockable': 2
	, 'unlock': 3
	, 'reserve': 1
	, 'ask_lock': 4
	, 'lock': 5
}
var TASK_TYPE_CODES = {
	  'chg_unl': 1
	, 'chg_ava': 2
	, 'chg_unu': 3
	, 'chg_use': 4
	, 'chg_off': 5
	, 'chg_res': 6
}

var FORBIDDEN_ZONES = {}

var DATABASE_POLL_INTERVAL = 1000 // milliseconds

exports.TABLE_NAMES = TABLE_NAMES
exports.TASK_STATES_CODES = TASK_STATES_CODES
exports.pgsql = pgsql
exports.DATABASE_POLL_INTERVAL = DATABASE_POLL_INTERVAL
exports.TASK_TYPE_CODES = TASK_TYPE_CODES
exports.USER_ACTION_CODES = USER_ACTION_CODES
exports.FORBIDDEN_ZONES = FORBIDDEN_ZONES