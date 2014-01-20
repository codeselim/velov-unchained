"use strict"

var pg = require('pg');
var conString = "postgres://velovunchained:velovunchained@localhost/velovunchained";

pg.connect(conString, function(err, client, done) {
  if(err) {
    return console.error('error fetching client from pool', err);
  }

  client.query('INSERT INTO task_types (name) VALUES (\'Hey\')', [], function(err, result) {

    if(err) {
      return console.error('error running query', err);
    }
    //output: 1
  });

  client.query('INSERT INTO velov_tasks (type) VALUES ($1::int)', ['1'], function(err, result) {
    //call `done()` to release the client back to the pool
    done();

    if(err) {
      return console.error('error running query', err);
    }
    //output: 1
  });
});