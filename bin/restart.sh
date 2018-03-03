#!/bin/bash

set -x
kill -9 $(ps aux | grep "Headless-Chrome" | grep -v grep | awk '{print $2}')
kill -9 $(ps aux | grep "node_modules" | grep -v grep | awk '{print $2}')
rm -rf /tmp/puppeteer_dev_profile-*
root=/home/ubuntu/kf-stock
nohup node $root/src/server.js Headless-Chrome > $root/logs/nohup.log 2>&1 &
