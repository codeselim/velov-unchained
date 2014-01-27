"use strict"

//* Server that deals with the data from the velovs

// Note: Network protocol is defined here https://docs.google.com/document/d/1ruhZYn532nGK_tueSa5HPL_cqe6Hj630zpdrcCcXIH4/edit#
var events = require('events');
var net = require("net");
var gps_utils = require("./gps_utils");
var tasks = require("./tasks");
var netw = require('./network')
var get_tile_from_gps_coords = gps_utils.get_tile_from_gps_coords
var sd = require('./shared_data')
var FRAME_SEPARATOR = netw.FRAME_SEPARATOR
var DATA_SEPARATOR = netw.DATA_SEPARATOR
var STATES_CODES = {}
var isPointInPoly = require('./point-in-poly').isPointInPoly
var FORBIDDEN_ZONES = sd.FORBIDDEN_ZONES
var DBG = true
var t = sd.TABLE_NAMES // handy shortcut, for even shorter use
var db = sd.pgsql

var decode = netw.decode

var action_localization = function (frame_data, stream) {
	var tile_index = get_tile_from_gps_coords(frame_data.params[2], frame_data.params[3])
	db.select_query
	db.insert_query(t['loc_histo'], ['velov_id', 'time', 'tile_index', 'lat', 'long'], [frame_data.params[0], frame_data.params[1], tile_index, frame_data.params[1], frame_data.params[2]], function (err, result) {
		console.log("Query has been executed.", err)
	})
}

var action_change_state = function (frame_data, stream) {
	if (frame_data.params[2] === 'USE') {
		// First, select the user that asked to lock this velov last (he's the one who's unlocking the velov right now)
		// Unless he's very unlucky and someone has beaten him and taken his velov from him!
		db.text_query(
			'SELECT user_id FROM '+ t['uah'] + ' WHERE velov_id = ' + frame_data.id + "ORDER BY id DESC LIMIT 1",
			function (err, result) {
				if (err) {
					console.error("Could not retrieve the user who asked to unlock this velov. error:", err)
				};
				if (!result.rows.length) {
					console.error("Somehow, nobody seems to have asked to unlock this bike but the velov is still asking to be unlocked")
					//TODO : Maybe somehow refuse to the velov to change state ?
				} else {
					var user_id = result.rows[0].user_id
					sd.pgsql.insert_query(
						t['uah'],
						['velov_id', 'user_id', 'time', 'action_id'],
						[frame_data.id, user_id, frame_data.time, sd.USER_ACTION_CODES['unlock']],
						function (err2, result2) {
							if (err) {
								console.error("ERR somethign went wrong while inserting the new user action")
							} else {
								sd.pgsql.insert_query(
									t['urs'],
									['user_id', 'velov_id', 'time_start'],
									[user_id, frame_data.id, frame_data.time]
								)
								update_velov_state_to(frame_data.id, frame_data.params[2], frame_data.time)
							}
						}
					)				
				}
			}
		)
	} else if (frame_data.params[2] === 'RLK') {
		// User asked to release the velov
		// First, let us see if it is allowed where the velov is currently, then, register that
		db.text_query(
			'SELECT user_id, id FROM '+ t['urs'] + ' WHERE velov_id = ' + frame_data.id + " AND time_end IS NULL ORDER BY id DESC LIMIT 1",
			function (err, result) {
				if (err || !result.rows.length) {
					console.error("Could not retrieve the user who is currently renting this velov error:", err, result)
					// Refuse lock
					netw.reply_velov(stream, {cmd: "REP", confirm: 'NOK', params:[]})
				} else {
					var user_id = result.rows[0].user_id
					var renting_session_id = result.rows[0].id
					sd.pgsql.insert_query(
						t['uah'],
						['velov_id', 'user_id', 'time', 'action_id'],
						[frame_data.id, user_id, frame_data.time, sd.USER_ACTION_CODES['ask_lock']],
						function (err2, result2) {
							if (err) {
								console.error("ERR somethign went wrong while inserting the new user action")
							} else {
								//TODO: Here, add something that checks for forbidden zones and answers NO if in such a zone
								var forbidden = false

								for (var i = 0; i < FORBIDDEN_ZONES.length; i++) {
									if (isPointInPoly(current_pos, FORBIDDEN_ZONES[i])) {
										forbidden = true
										break
									};
								};

								if (forbidden) {
									netw.reply_velov(stream, {cmd: "REP", confirm: 'NOK', params:[]}, function (success, original_data) {
										if (success) {
											stream.end()
											stream.destroy()
										} else {
											console.error("Could not reply to velov to allow unlocking...")
										}
								} else {
									netw.reply_velov(stream, {cmd: "REP", confirm: 'OK', params:[]}, function (success, original_data) {
										if (success) {
											stream.end()
											stream.destroy()
											sd.pgsql.update_query(
												t['urs'],
												['time_end'],
												[frame_data.time],
												['id'],
												[renting_session_id]
											)
										} else {
											console.error("Could not reply to velov to allow unlocking...")
										}
									})
								}
							}
						}
					)				
				}
			}
		)
	} else {
		update_velov_state_to(frame_data.id, frame_data.params[2], frame_data.time)
	}
}

var update_velov_state_to = function (velov_id, new_state_codename, time) {
	db.insert_query(
		t['sh'],
		['velov_id', 'state_id', 'time'],
		[velov_id, STATES_CODES[new_state_codename], time],
		function (err, result) {
			console.log("Velov", velov_id, "has been registered as in state", new_state_codename)
		}
	)
}

var frame_actions = {
	  "LOC": action_localization
	, "CHG": action_change_state
}

var frame_action = function (frame_data, stream) {
	if (!(frame_data.type in frame_actions)) {
		console.error("Received command of type ", frame_data.type, ", not recognized, doing nothing.")
		return false
	}
	return frame_actions[frame_data.type](frame_data, stream)
}

function start (db, port) {
	db.select_query(t['s'], ['id', 'codename'], null, null, null, function (err, result) {
		if (err) {
			console.error("An error occured while loading velov states:", err, "aborting server start.")
			return false
		};
		for (var i = 0; i < result.rows.length; i++) {
			STATES_CODES[result.rows[i].codename] = result.rows[i].id
		};

		db.select_query(t['fz'], ['*'], null, null, null, function (err, result) {
			if (err) {
				console.error("An error occured while loading velov states:", err, "aborting server start.")
				return false
			};
			for (var i = 0; i < result.rows.length; i++) {
				if (result.rows[i].id in FORBIDDEN_ZONES) {
					FORBIDDEN_ZONES[result.rows[i].id].push({'lat': result.rows[i].lat, 'long': result.rows[i].long})	
				} else {
					FORBIDDEN_ZONES[result.rows[i].id] = [{'lat': result.rows[i].lat, 'long': result.rows[i].long}]	
				}
			};

			console.log("Loaded the following forbidden zones: ", FORBIDDEN_ZONES)

			var server = net.createServer(function(stream) {
				stream.setTimeout(0);
				stream.setEncoding("utf8");

				stream.addListener("connect", function(){
					console.log("VSERV: ", new Date(), "New velovs server connection established.")
				});

				var buffer = ""
				stream.addListener("data", function (data) {
					console.log("VSERV: ", new Date(), "Receiving data from a velov.")
					buffer += data
					var pos = -1
					while (-1 != (pos = buffer.indexOf(FRAME_SEPARATOR))) {//* We have found a separator, that means that the previous frame (that may be incomplete or may not) is over and a new one starts
						console.log(new Date(), "A frame is over")
						console.log(buffer)
						console.log(buffer.indexOf(FRAME_SEPARATOR))
						// console.log("pos=", pos)
						var frame = buffer.substr(0, pos)
						buffer = buffer.substr(pos + FRAME_SEPARATOR.length, buffer.length) //* If the second parameter is >= the maximum possible length substr can return, substr just returns the maximum length possible, so who cares substracting?
						var frame_data = decode(frame)
						frame_action(frame_data, stream)
					};
					console.log("VSERV: ", "Ending the velovs stream data receiver function") //* Mainly for the purpose of being able to check when the VELOV_FRAME_EVENT handler function is executed with respect to the current function execution
				});

				stream.addListener("end", function() {
					console.log("VSERV: ", "Closing a velovs server connection")

					stream.end();
				});
			});

			server.listen(port);
		})
	})

	setInterval(function () {
		tasks.check_for_tasks(db)
	}, sd.DATABASE_POLL_INTERVAL);

	//TODO: Remove this test code:
	// setInterval(function () {
	// 	message_velov(0, {ip: '192.168.43.56'}, null)
	// }, 1000)

}

exports.start = start
exports.update_velov_state_to = update_velov_state_to
