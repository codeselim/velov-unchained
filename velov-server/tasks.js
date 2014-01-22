"use strict"

var sd = require('./shared_data')
var t = sd.TABLE_NAMES
var TASK_STATES_CODES = sd.TASK_STATES_CODES
var netw = require('./network')
var check_for_tasks = function (db) {
	db.select_query(t['t'], ['*'], ['task_state_id'], [TASK_STATES_CODES['todo']], null, function (err, result) {
		
		if (err) {
			console.error("Could not retrieve list of todo tasks.", err)
		} else {
			console.log("The following task were retrieved and have to be processed", result)
		}

		if (!result.rows.length) {
			return // Nothing to do
		};

		var ids = ""
		var comma = ""
		for (var i = 0; i < result.rows.length; i++) {
			ids += comma + result.rows[i].id
			comma = ","
		};
		db.text_query('UPDATE ' + t['t'] + " SET task_state_id = '" + TASK_STATES_CODES['inprogress'] + "' WHERE id IN(" + ids + ")" , 
			function (err2, result2) {
				if (err2) {
					console.error("Something went wrong when trying to set as pending, tasks that were for current run.", err2, result2)
				};
				process_tasks(result)
		})
	})
}

var process_tasks = function (tasks_from_db) {
	for (var i = 0; i < tasks_from_db.rows.length; i++) {
		switch (tasks_from_db.rows[i].type) {
			case 1:// Change state to unlockable
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						params: ['UNL']
					},
					function () {
						console.log("Message sent to velov.")
					}
				)
				break;
			case 2:// Change state to available
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						params: ['AVA']
					},
					function () {
						console.log("Message sent to velov.")
					}
				)
				break;
			case 3:// Change state to NOT available (Unusable)
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						params: ['UNU']
					},
					function () {
						console.log("Message sent to velov.")
					}
				)
				break;
			case 4:// Change state to In Use
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						params: ['USE']
					},
					function () {
						console.log("Message sent to velov.")
					}
				)
				break;
			case 5:// Change state to Off
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						params: ['OFF']
					},
					function () {
						console.log("Message sent to velov.")
					}
				)
				break;
			case 6:// Change state to Reserved
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						params: ['RES']
					},
					function () {
						console.log("Message sent to velov.")
					}
				)
				break;
		}
	};
}

exports.check_for_tasks = check_for_tasks