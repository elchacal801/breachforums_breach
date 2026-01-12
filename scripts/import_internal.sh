#!/bin/bash
# Optimized import with transactions
(echo "SET autocommit=0; SET unique_checks=0; SET foreign_key_checks=0;"; grep '^INSERT INTO' /tmp/dump.sql; echo "COMMIT;") | mysql -uroot -presearch_only bf --init-command="SET sql_mode=''"
