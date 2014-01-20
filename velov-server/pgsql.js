"use strict"

var pg = require('pg');
var conString = "postgres://velovunchained:velovunchained@localhost/velovunchained";

var client = new pg.Client(conString)

client.connect()

var insert_query = function (table_name, columns, values, callback) {
	var values_params = []
	var comma = ''
	for (var i = 0; i < values.length; i++) {
		values_params += comma + "$" + i
		comma = ', '
	};
	client.query("INSERT INTO " + table_name + " (" + columns.join(", ") + ") VALUES (" + values_params + ")", values , callback)
}

var update_query = function (table_name, columns, values, callback) {
	var values_params = []
	var comma = ''
	for (var i = 0; i < values.length; i++) {
		values_params += comma + columns[i] + "=$" + i
		comma = ', '
	};
	client.query("UPDATE " + table_name + " SET " + values_params, values , callback)
}

var delete_query = function (table_name, columns, values, operator, callback) {
	var values_params = []
	if (typeof operator == "undefined" || !operator) {
		var operator = " AND "
	} else {
		operator = " " + operator + " "
	}
	var comma = ''
	for (var i = 0; i < values.length; i++) {
		values_params += comma + columns[i] + "=$" + i
		comma = operator
	};
	client.query("DELETE FROM " + table_name + " WHERE " + values_params, values , callback)
}
