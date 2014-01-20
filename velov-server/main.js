server = require('./server')
pgsql = require('./pgsql')

server.start(pgsql, 3000)