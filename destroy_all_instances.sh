#!/bin/bash

# Get list of instances in raw format
INSTANCES=$(./vast show instances --raw)

# Extract IDs using jq (a lightweight JSON processor) and iterate over them
echo "$INSTANCES" | jq -r '.[].id' | while read -r ID; do
    echo "Destroying instance with ID: $ID"
    ./vast destroy instance $ID
done
