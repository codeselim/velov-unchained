"use strict"

//* Server that deals with the data from the velovs


var events = require('events');
var net = require("net");
var FRAME_SEPARATOR = "\n"

var decode = function (frame) {
	return frame
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
			};
			// console.log("VSERV: ", "Ending the velovs stream data receiver function") //* Mainly for the purpose of being able to check when the VELOV_FRAME_EVENT handler function is executed with respect to the current function execution
		});

		stream.addListener("end", function(){
			console.log("VSERV: ", "Closing a velovs server connection")

			stream.end();
		});
	});

	server.listen(port);
}

exports.start = start
