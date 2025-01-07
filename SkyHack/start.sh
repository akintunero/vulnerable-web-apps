#!/bin/bash

echo "Starting SkyHack Airlines Application..."

echo "Cleaning up previous database..."
rm -f database/airline.db

echo "Initializing fresh database..."
python init_db.py

echo "Starting Flask application..."
python app.py 