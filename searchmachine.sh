#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <machine_id>"
    exit 1
fi

# Run the vast search command with the provided machine ID
./vast search offers "machine_id=$1 verified=any rentable=any"
