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
			console.log("The following task were retrieved and have to be processed", result.rows)
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

var process_chg_state_velov_reply = function (reply_data, original_data) {
	console.log("Message sent to velov. And it replied (task_id=", original_data.task_id, ")")
	if (reply_data.cmd === "REP") {
		if (reply_data.params[0] == "OK") {
			console.log("Velov answered OK")
			sd.pgsql.update_query(t['t'], ['task_state_id'], [TASK_STATES_CODES['success']], ['id'], [original_data.task_id], null, function (err, result) {
				if (err) {
					console.error("Something went wrong while trying to set the task as successfull")
				};
			})
		} else if (reply_data.params[0] == "NOK") {
			console.log("Velov answered NOK")
			sd.pgsql.update_query(t['t'], ['task_state_id'], [TASK_STATES_CODES['failure']], ['id'], [original_data.task_id], null, function (err, result) {
				if (err) {
					console.error("Something went wrong while trying to set the task as successfull")
				};
			})
		} else {
			console.error("Velov answered", reply_data.params[0], "which is not a valid REPly parameter")
		}
	};
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
						task_id: tasks_from_db.rows[i].id,
						params: ['UNL']
					},
					process_chg_state_velov_reply
				)
				break;
			case 2:// Change state to available
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						task_id: tasks_from_db.rows[i].id,
						params: ['AVA']
					},
					process_chg_state_velov_reply
				)
				break;
			case 3:// Change state to NOT available (Unusable)
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						task_id: tasks_from_db.rows[i].id,
						params: ['UNU']
					},
					process_chg_state_velov_reply
				)
				break;
			case 4:// Change state to In Use
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						task_id: tasks_from_db.rows[i].id,
						params: ['USE']
					},
					process_chg_state_velov_reply
				)
				break;
			case 5:// Change state to Off
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						task_id: tasks_from_db.rows[i].id,
						params: ['OFF']
					},
					process_chg_state_velov_reply
				)
				break;
			case 6:// Change state to Reserved
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						task_id: tasks_from_db.rows[i].id,
						params: ['RES']
					},
					process_chg_state_velov_reply
				)
				break;
		}
	};
}

exports.check_for_tasks = check_for_tasks