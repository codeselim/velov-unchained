"use strict"

var sd = require('./shared_data')
var t = sd.TABLE_NAMES
var TASK_STATES_CODES = sd.TASK_STATES_CODES
var check_for_tasks = function (db) {
	db.select_query(t['t'], ['*'], ['status'], [TASK_STATES_CODES['todo']], function (err, result) {
		
		if (err) {
			console.error("Could not retrieve list of todo tasks.", err)
		};

		var ids = ""
		var comma = ""
		for (var i = 0; i < result.row.length; i++) {
			ids += comma + result.row[i].id
			comma = ","
		};
		db.text_query('UPDATE ' + t['t'] + "SET status = '" + TASK_STATES_CODES['inprogress'] + "' WHERE id IN(" + ids + ")" , function (err2, result2) {
			if (err2) {
				console.error("Something went wrong when trying to set as pending, tasks that were for current run.", err2, result2)
			};
			process_tasks(result2)
		})
	})
}

var process_tasks = function (tasks_from_db) {
	for (var i = 0; i < tasks_from_db.row.length; i++) {
		switch (tasks_from_db.row[i].type) {
			case 1:// Change state to unlockable
				//TODO
				break;
		}
	};
}

exports.check_for_tasks = check_for_tasks