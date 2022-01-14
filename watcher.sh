#!/usr/bin/env bash

# This little utility notices when the timestamps change in this directory
# and then reruns the pdf generator script. If you have something like
# evince running that reloads the PDF when it changes this can be very
# convenient.
watch -g ls -l *.py *.sh *.png; echo "Something changed. Sleeping 1..."; sleep 1; ./vast.py generate pdf-invoices; ./watcher.sh