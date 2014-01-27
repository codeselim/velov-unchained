#!/bin/bash

## This assumes DB has already been created and the role too
psql -U velovunchained -W -d postgres < schema.sql
psql -U velovunchained -W -d velovunchained < data.sql

