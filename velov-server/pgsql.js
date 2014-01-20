"use strict"

var pg = require('pg');
var conString = "postgres://velovunchained:velovunchained@localhost/velovunchained";

pg.connect(conString, function(err, client, done) {
  if(err) {
    return console.error('error fetching client from pool', err);
  }
  client.query('SELECT $1::int AS numbor', ['1'], function(err, result) {
    //call `done()` to release the client back to the pool
    done();

    if(err) {
      return console.error('error running query', err);
    }
    console.log(result.rows[0].numbor);
    //output: 1
  });
});