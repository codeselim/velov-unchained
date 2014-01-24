"use strict"

var VELOV_MESSAGE_FAILED_RETRY_TIME = 5000 // milliseconds
var VELOV_CONNECTION_PORT = 5000
var net = require('net')
var crypto = require('crypto')
var FRAME_SEPARATOR = "\n"
var DATA_SEPARATOR = "\t"
var CMD_LEN = 3 // length of the string expressing the  "command" in a frame from the velov
var MAX_VELOV_MSG_OR_REP_RETRY = 60 // retry 20 times to contact a given velov before giving up

var sha1 = function (string) {
	var sha1sum = crypto.createHash('sha1')
	sha1sum.update(string)
	return sha1sum.digest('hex')
}

var DBG = true

var message_velov = function (data_to_send, callback, tries_count) {
	var sock = new net.Socket()

	if (typeof tries_count == "undefined" || tries_count === null) {
		tries_count = 1
	};

	if (tries_count > MAX_VELOV_MSG_OR_REP_RETRY) {
		callback(null, data_to_send, false)
	};

	var message = create_frame_from_data(data_to_send)
	
	// TODO: Add some SSL security to this connection...
	sock.connect(VELOV_CONNECTION_PORT, data_to_send.ip, function () { 
		console.log('message_velov: Connection to velov ' + data_to_send.velov_id + ' established, going to send: ', message)
		sock.write(message, null, function () {
			console.log('message_velov: Data sent to velov.')
		})
	})

	var buffer = ""
	sock.addListener("data", function (reply_frame_buffer) {
		console.log(Date.now(), "Velov said:", reply_frame_buffer.toString())
		buffer += reply_frame_buffer
		var pos = -1
		while (-1 != (pos = buffer.indexOf(FRAME_SEPARATOR))) {//* We have found a separator, that means that the previous frame (that may be incomplete or may not) is over and a new one starts
			var frame = buffer.substr(0, pos)
			buffer = buffer.substr(pos + FRAME_SEPARATOR.length, buffer.length) //* If the second parameter is >= the maximum possible length substr can return, substr just returns the maximum length possible, so who cares substracting?
			var reply_data = decode(frame)
			console.log("messave_velov(): Launching callback")
			callback(reply_data, data_to_send)
		};
	});

	sock.on("error", function () { 
		console.error("message_velov:", new Date().toString() + "Could not send message " + message + "to velov " + data_to_send.velov_id + ", trying again in 10 seconds."); 
		setTimeout(function () {
			message_velov(data_to_send, callback, tries_count+1)
		}, VELOV_MESSAGE_FAILED_RETRY_TIME)
	})
}

var reply_velov = function (stream, data_to_send, callback, tries_count) {

	if (typeof tries_count == "undefined" || tries_count === null) {
		tries_count = 1
	};

	if (tries_count > MAX_VELOV_MSG_OR_REP_RETRY) {
		callback(false, data_to_send)
	};

	var message = create_frame_from_data(data_to_send)
	stream.write(message, null, function () {
		console.log('message_velov: Data sent to velov.')
		callback(true, data_to_send)
	})

	stream.on("error", function () { 
		console.error("message_velov:", new Date().toString() + "Could not send message " + message + "to velov " + data_to_send.velov_id + ", trying again in 10 seconds."); 
		setTimeout(function () {
			message_velov(stream, data_to_send, callback, tries_count+1)
		}, VELOV_MESSAGE_FAILED_RETRY_TIME)
	})

}

var decode = function (frame, is_rep) {
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
		, 'id': (!is_rep) ? parseInt(params[0]) : null // When it's a reply, is not specified
		, 'time': (!is_rep) ? parseInt(params[1]) : parseInt(params[0]) // When it's a reply, is not specified, thus timestamp is 2nd param
		, 'raw_frame': frame // Can be useful in some cases
	}

	if (DBG) {
		console.log("decode(),frame=", frame, "result=", result)
	};

	return result
}

var checksum = function (data) {
	return sha1(data)
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
	return (netw.checksum(data) === data_checksum)
}


var create_frame_from_data = function (data) {
	if (data.cmd === "REP") {
		// Special REP frame is special
		var frame = data.cmd + " " + data.confirm + data.params.join(" ") + " " + Date.now()
	} else {
		var frame = data.cmd + ((data.velov_id) ? " " + data.velov_id : "") + " " + Date.now() + " " + data.params.join(" ")
	}
	var c = checksum(frame)
	frame += "\t" + c + "\n"
	if (DBG) {
		console.log("Consituted frame:\n", frame, "\n from data:", data)
	};
	return frame
}

exports.message_velov = message_velov
exports.reply_velov = reply_velov
exports.create_frame_from_data = create_frame_from_data
exports.checksum = checksum
exports.FRAME_SEPARATOR = FRAME_SEPARATOR
exports.DATA_SEPARATOR = DATA_SEPARATOR
exports.decode = decode