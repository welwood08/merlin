#!/bin/bash
echo "Dumping old database..."
./dump_db.sh $1
echo "Clearing old database..."
./empty_tables.sh
echo "Repopulating database..."
python createdb.py --new
echo "Complete!"
