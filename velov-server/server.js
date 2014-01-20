"use strict"

//* Server that deals with the data from the velovs

// Note: Network protocol is defined here https://docs.google.com/document/d/1ruhZYn532nGK_tueSa5HPL_cqe6Hj630zpdrcCcXIH4/edit#
var events = require('events');
var net = require("net");
var FRAME_SEPARATOR = "\n"
var DATA_SEPARATOR = "\t"
var sha1sum = require('crypto').createHash('sha1')
var VELOV_CONNECTION_PORT = 5000
var VELOV_MESSAGE_FAILED_RETRY_TIME = 10000 // milliseconds
var CMD_LEN = 3 // length of the string expressing the  "command" in a frame from the velov

var sha1 = function (string) {
	sha1sum.update(string)
	return sha1sum.digest('hex')
}

var decode = function (frame) {
	var data = get_data_from_frame(frame)
	var type = get_type_from_data(data)
	var cmd = get_cmd_from_data(data)
	var params = get_params_from_data(data)
	return {
		  'type': type
		, 'cmd': cmd
		, 'params': params
	}
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

var create_frame_from_data = function (data) {
	return "HLO\n" // TODO actually implement this
}

var message_velov = function (velov, data, callback, tries_count) {
	var sock = new net.Socket()

	var message = create_frame_from_data(data)
	
	// TODO: Add some SSL security to this connection...
	sock.connect(VELOV_CONNECTION_PORT, data.ip, function () { 
		console.log('message_velov: Connection to velov ' + velov + ' established, going to send: ', message)
		sock.write(message, null, function () {
			sock.end()
			sock.destroy()
			console.log('message_velov: Data sent to velov, disconnecting.')
			console.log("Exiting in message_velov() callback")
		})
		// The following code was originally in the write() callback BUT. As the data is less than the kernel io buffer, it seems there a kind of a bug in nodejs and the callback s called extremely long after, not to say never
		// So just consider the data was written: 
		if (null != callback) {
			callback()
		};
	})

	sock.on("error", function () { 
		console.error("message_velov:", new Date().toString() + "Could not send message " + message + "to velov " + velov + ", trying again in 10 seconds."); 
		if (tries_count == null) {
			tries_count = 1
		};
		setTimeout(function () {
			message_velov(velov, data, callback, tries_count+1)
		}, VELOV_MESSAGE_FAILED_RETRY_TIME)
	})
}

var action_localization = function (frame_data) {
	frame_data.params
}
var frame_actions = {
	"LOC": action_localization
}

var frame_action = function (frame_data) {
	frame_actions[frame_data.frame_type](frame_data)
}

function start (db, port) {
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
				frame_action(frame_data)
			};
			console.log("VSERV: ", "Ending the velovs stream data receiver function") //* Mainly for the purpose of being able to check when the VELOV_FRAME_EVENT handler function is executed with respect to the current function execution
		});

		stream.addListener("end", function(){
			console.log("VSERV: ", "Closing a velovs server connection")

			stream.end();
		});
	});

	server.listen(port);

	//TODO: Remove this test code:
	setInterval(function () {
		message_velov(0, {ip: '127.0.0.1'}, null)
	}, 1000)

}

exports.start = start
