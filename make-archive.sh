#!/usr/bin/env bash


mkdir vast.ai
# cp -a venv vast.ai
cp -a vast.ai-logo.png vast.py vast_pdf.py vast.ai
tar cvzf vast.tar.gz vast.ai
rm -rf vast.ai
