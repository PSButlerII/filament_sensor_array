# Pico Spool Monitor v2 - Phase 2 No Microdot

This phase removes Microdot completely.

Upload to Pico root:
- main.py
- config.py
- sensors.py
- state.py
- wifi_manager.py
- http_server.py

No microdot.py or microdot_asyncio.py needed.

Endpoints:
- GET /
- GET /api/health
- GET /api/dashboard
- POST /api/wifi/save

First Wi-Fi setup:
If there are no saved profiles, the Pico starts AP mode.

SSID: PicoSpoolSetup
Password: pico-setup

Save a Wi-Fi profile:

curl -X POST http://192.168.4.1/api/wifi/save \n  -H "Content-Type: application/json" \n  -d '{"ssid":"YOUR_WIFI","password":"YOUR_PASSWORD","priority":1}'

Then fully power-cycle the Pico.

Test:
http://<pico-ip>/api/health
http://<pico-ip>/api/dashboard

# Pico Spool Monitor v2 - Phase 3 Dashboard

This phase adds a lightweight HTML dashboard with one API call.

Upload to Pico root:
- main.py
- config.py
- sensors.py
- state.py
- wifi_manager.py
- http_server.py
- portal.html

No Microdot needed.

Endpoints:
- GET /
- GET /api
- GET /api/health
- GET /api/dashboard
- POST /api/wifi/save

Dashboard behavior:
- one fetch to /api/dashboard
- refresh every 5 seconds
- no Wi-Fi scan
- no multiple endpoint polling