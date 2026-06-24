#!/bin/bash
cd "$(dirname "$0")"
python -m py_compile datasources/lark_drive.py
dify plugin package . -o lark-drive.difypkg
echo "Plugin packaged successfully!"
