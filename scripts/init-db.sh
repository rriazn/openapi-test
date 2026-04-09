#!/bin/bash

hatch run backend-cli reset-db
hatch run backend-cli import-users ./Users.csv
hatch run backend-cli import-exercises ./Exercises.csv