"use strict"

var VELOV_MESSAGE_FAILED_RETRY_TIME = 10000 // milliseconds
var VELOV_CONNECTION_PORT = 5000
var net = require('net')

var message_velov = function (velov, data, callback, tries_count) {
	var sock = new net.Socket()

	if (typeof tries_count == "undefined" || tries_count === null) {
		tries_count = 1
	};

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
		setTimeout(function () {
			message_velov(velov, data, callback, tries_count+1)
		}, VELOV_MESSAGE_FAILED_RETRY_TIME)
	})
}

var create_frame_from_data = function (data) {
	return data.message + "\n" // TODO actually implement this
}

exports.message_velov = message_velov
exports.create_frame_from_data = create_frame_from_data