@echo off
echo =========================================
echo  TIME VARIANCE AUTHORITY - PROXY UPLINK
echo =========================================
set /p port="ENTER LOCAL PORT FOR UPLINK: "
set SERVER_URL=wss://tunnell.onrender.com
node src/client.js --port %port% --subdomain tunnell
pause
