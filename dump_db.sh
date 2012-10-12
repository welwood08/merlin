#!/bin/bash
mysqldump -xuroot -p merlin > mysql-merlin-`date +"%Y%m%d.%H%M%S"`_$1.sql
