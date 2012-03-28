#!/bin/bash
for i in {18..114}
do
   echo "Tick $i"
   perl -pi -w -e "s/tk\/$(($i-1))/tk\/$i/g;" merlin.cfg
   python excalibur.py
done
