"use strict"

var sd = require('./shared_data')
var t = sd.TABLE_NAMES
var TASK_STATES_CODES = sd.TASK_STATES_CODES
var netw = require('./network')

var server = require('./server')

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

var register_user_action = function (success, reply_data, original_data) {
	if (!success) {
		return
	};
	var task = original_data.task
	if (task.type == sd.TASK_TYPE_CODES['chg_unl']) {
		// The user asked to set the velov to unlockable and is has bee done with success
		// then, register it into the db
		sd.pgsql.insert_query(
			t['uah'],
			['velov_id', 'user_id', 'time', 'action_id'],
			[task.velov_id, task.user_id, reply_data.time, sd.USER_ACTION_CODES['ask_unlockable']],
			function (err, result) {
				if (err) {
					console.error("ERR somethign went wrong while inserting the new user action")
				};
			}
		)
	};
	if (task.type == sd.TASK_TYPE_CODES['chg_res']) {
		// The user asked to set the velov to unlockable and is has bee done with success
		// then, register it into the db
		sd.pgsql.insert_query(
			t['uah'],
			['velov_id', 'user_id', 'time', 'action_id'],
			[task.velov_id, task.user_id, reply_data.time, sd.USER_ACTION_CODES['reserve']],
			function (err, result) {
				if (err) {
					console.error("ERR somethign went wrong while inserting the new user action")
				};
			}
		)
	};
}

var process_chg_state_velov_reply = function (reply_data, original_data) {
	console.log("Message sent to velov. And it replied (task.id=", original_data.task.id, ")")
	if (!reply_data) {
		console.error("It replied nothing, aborting");
		return
	};
	if (reply_data.cmd === "REP") {
		if (reply_data.params[0] == "OK") {
			console.log("Velov answered OK")
			sd.pgsql.update_query(t['t'], ['task_state_id'], [TASK_STATES_CODES['success']], ['id'], [original_data.task.id], null, function (err, result) {
				if (err) {
					console.error("Something went wrong while trying to set the task as successfull")
				} else {
					register_user_action(true, reply_data, original_data)
				}
			})
			// Register the new state of the velov
			server.update_velov_state_to(original_data.task.velov_id, reply_data.params[2], reply_data.params[1])
		} else if (reply_data.params[0] == "NOK") {
			console.log("Velov answered NOK")
			sd.pgsql.update_query(t['t'], ['task_state_id'], [TASK_STATES_CODES['failure']], ['id'], [original_data.task.id], null, function (err, result) {
				if (err) {
					console.error("Something went wrong while trying to set the task as successfull")
				} else {
					register_user_action(false, reply_data, original_data)
				}
			})
		} else {
			console.error("Velov answered", reply_data.params[0], "which is not a valid REPly parameter")
		}
	};
}

var process_tasks = function (tasks_from_db) {
	for (var i = 0; i < tasks_from_db.rows.length; i++) {
		var task = tasks_from_db.rows[i]
		switch (task.type) {
			case 1:// Change state to unlockable
				netw.message_velov(
					{
						velov_id: 1 /* TODO CHANGE THAT TO THE ACTUAL VELOV TO BE CONTACTED */,
						'ip': '127.0.0.1',
						'cmd': 'CHG',
						'task': task,
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
						'task': task,
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
						'task': task,
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
						'task': task,
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
						'task': task,
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
						'task': task,
						params: ['RES']
					},
					process_chg_state_velov_reply
				)
				break;
		}
	};
}

exports.check_for_tasks = check_for_tasks