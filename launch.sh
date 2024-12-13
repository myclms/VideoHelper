#!/bin/bash
source launchpy.sh &
clipid=$!
echo "clipid: $clipid"
sleep 1

echo "...... lauch google-chrome ......"
google-chrome --new-window index.html --disable-web-security --user-data-dir=tmp

wait $clipid
