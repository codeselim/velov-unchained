"use strict"

var server = require('./server')
var shared_data = require('./shared_data')

server.start(shared_data.pgsql, 3000)