#!/bin/bash

echo "Starting VoteVault application..."

# Remove any existing database to prevent locking issues
rm -f voting.db

# Initialize the application
python app.py 