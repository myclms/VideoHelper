#!/bin/bash
source launchpy.sh &
clipid1=$!
echo "py_pid: $clipid1"
sleep 1

source launchdeeplx.sh &
clipid2=$!
echo "deeplx_pid: $clipid2"
sleep 1

echo "...... lauch google-chrome ......"
google-chrome --new-window index.html --disable-web-security --user-data-dir=tmp --incognito --start-maximized

wait $clipid1
wait $clipid2
