"use strict"

//* Server that deals with the data from the velovs

// Note: Network protocol is defined here https://docs.google.com/document/d/1ruhZYn532nGK_tueSa5HPL_cqe6Hj630zpdrcCcXIH4/edit#
var events = require('events');
var net = require("net");
var gps_utils = require("./gps_utils");
var tasks = require("./tasks");
var get_tile_from_gps_coords = gps_utils.get_tile_from_gps_coords
var FRAME_SEPARATOR = "\n"
var DATA_SEPARATOR = "\t"
var sha1sum = require('crypto').createHash('sha1')
var CMD_LEN = 3 // length of the string expressing the  "command" in a frame from the velov
var STATES_CODES = {}

var DBG = true
var sd = require('./shared_data')
var t = sd.TABLE_NAMES // handy shortcut, for even shorter use

var sha1 = function (string) {
	sha1sum.update(string)
	return sha1sum.digest('hex')
}

var decode = function (frame) {
	var data = get_data_from_frame(frame)

	if (DBG) {
		console.log("decode(), data=", data)
	};

	var type = get_type_from_data(data)
	var cmd = get_cmd_from_data(data)
	var params = get_params_from_data(data)
	var result = {
		  'type': type
		, 'cmd': cmd
		, 'params': params
	}

	if (DBG) {
		console.log("decode(),frame=", frame, "result=", result)
	};

	return result
}

/**
 * @return the command, extracted from the data, such as "CHG" for a state change, "LOC" for a localization command, etc. ...
*/
var get_cmd_from_data = function (data) {
	return data.substr(0, CMD_LEN)
}


/**
 * @return the type of the frame, extracted from the data, such as "CHG" for a state change, "LOC" for a localization command, etc. ...
*/
var get_type_from_data = function (data) {
	 // current implementation is the same as returning the cmd but we might want 
	 // to change this in the future so we keep this a separate function
	return get_cmd_from_data(data)
}

/**
@return an array of space-separated parameters of the given data
*/
var get_params_from_data = function (data) {
	return data.substr(CMD_LEN+1, data.length).split(" ")
}

var checksum = function (data) {
	return sha1(data)
}

var get_data_from_frame = function (frame) {
	var data_end_pos = frame.indexOf(DATA_SEPARATOR)
	var data = frame.substr(0, data_end_pos)
	return data
}

var get_checksum_from_frame = function (frame) {
	var data_end_pos = frame.indexOf(DATA_SEPARATOR)
	var data_checksum = frame.substr(data_end_pos + data_end_pos.length, frame.length)
	return data_checksum
}

var check_checksum = function (frame) {
	var data = get_data_from_frame(frame)
	var data_checksum = get_checksum_from_frame(frame)
	return (checksum(data) === data_checksum)
}

var action_localization = function (frame_data, db) {
	var tile_index = get_tile_from_gps_coords(frame_data.params[2], frame_data.params[3])
	db.select_query
	db.insert_query(t['loc_histo'], ['velov_id', 'time', 'tile_index', 'lat', 'long'], [frame_data.params[0], frame_data.params[1], tile_index, frame_data.params[1], frame_data.params[2]], function (err, result) {
		console.log("Query has been executed.", err)
	})
}

var action_change_state = function (frame_data, db) {
	db.insert_query(t['sh'], ['velov_id', 'state_id', 'time'], [frame_data.params[0], STATES_CODES[frame_data.params[2]], frame_data.params[1]], function (err, result) {
		console.log("Query has been executed.", err)
	})
}

var frame_actions = {
	  "LOC": action_localization
	, "CHG": action_change_state
}

var frame_action = function (frame_data, db) {
	if (!(frame_data.type in frame_actions)) {
		console.error("Received command of type ", frame_data.type, ", not recognized, doing nothing.")
		return false
	}
	return frame_actions[frame_data.type](frame_data, db)
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
					frame_action(frame_data, db)
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

	setInterval(function () {
		tasks.check_for_tasks(db)
	}, 5000);

	//TODO: Remove this test code:
	// setInterval(function () {
	// 	message_velov(0, {ip: '192.168.43.56'}, null)
	// }, 1000)

}

exports.start = start
