"use strict"

var TABLE_NAMES = { // shortens the code, and avoids spelldraws, in short, THIS IS [SPARTA?] CONSTANTS!
	  'loc_histo': "velov_location_history"
	, 't': "velov_tasks"
	, 'tt': "task_types"
	, 'sh': "velov_state_history"
	, 's': "states"
}

var TASK_STATES_CODES = {
	  'todo': 1
	, 'inprogress': 2
	, 'success': 3
	, 'failure': 4
}

exports.TABLE_NAMES = TABLE_NAMES
exports.TASK_STATES_CODES = TASK_STATES_CODES