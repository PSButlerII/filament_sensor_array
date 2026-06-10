# api.py
from microdot import Microdot, Response
import wifi_manager
import config

Response.default_content_type = "application/json"

def create_app(get_dashboard_payload):
    app = Microdot()

    @app.get("/")
    async def index(request):
        return {
            "message": "Pico Spool Monitor v2 API",
            "dashboard": "/api/dashboard",
            "health": "/api/health"
        }

    @app.get("/api/health")
    async def health(request):
        return {"ok": True, "device": config.DEVICE_NAME}

    @app.get("/api/dashboard")
    async def dashboard(request):
        return get_dashboard_payload()

    @app.post("/api/wifi/save")
    async def wifi_save(request):
        data = request.json or {}
        ssid = data.get("ssid")
        password = data.get("password", "")
        priority = data.get("priority", 10)

        if not ssid:
            return {"ok": False, "message": "ssid is required"}, 400

        wifi_manager.save_or_update_profile(ssid, password, priority)
        return {"ok": True, "ssid": ssid, "priority": priority}

    return app
