"use strict"

var get_tile_from_gps_coords = function (lat, long) {
	// TODO: Put all those constants INTO CONSTANTS!
	var tile_height = 0.01
	var tile_width = 0.01
	var tiles_per_row = 10
	var max_row = 10
	// Origin (top-left corner) coordinates
	var O_lat = 45.8
	var O_long = 4.77

	if (lat > O_lat || lat < (O_lat - tile_height*max_row) || long < O_long || long > (O_long + tile_width*tiles_per_row)) {
		console.error("Asked for index of coords ", lat, ",", long, " which is out of the grid" )
		return -1
	};

	var lat_delta = Math.abs(lat - O_lat)
	var long_delta = long - O_long

	var row = Math.ceil(lat_delta / tile_height) - 1
	var col = Math.ceil(long_delta / tile_width) - 1

	var index = row * tiles_per_row + col
	return index
}

exports.get_tile_from_gps_coords = get_tile_from_gps_coords