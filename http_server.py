# http_server.py
import uasyncio as asyncio
import ujson as json


def http_response(body, status="200 OK", content_type="application/json"):
    if isinstance(body, (dict, list)):
        body = json.dumps(body)

    if not isinstance(body, str):
        body = str(body)

    return (
        "HTTP/1.1 %s\r\n"
        "Content-Type: %s\r\n"
        "Connection: close\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
        "%s"
    ) % (status, content_type, len(body), body)


def parse_request_line(line):
    try:
        parts = line.decode().split()
        return parts[0], parts[1]
    except Exception:
        return None, None


async def read_request(reader):
    first = await reader.readline()
    method, path = parse_request_line(first)

    content_length = 0

    while True:
        line = await reader.readline()

        if line == b"\r\n" or line == b"":
            break

        lower = line.lower()

        if lower.startswith(b"content-length:"):
            try:
                content_length = int(line.split(b":", 1)[1].strip())
            except Exception:
                content_length = 0

    body = b""

    if content_length > 0:
        body = await reader.read(content_length)

    return method, path, body


class TinyHttpServer:
    def __init__(
        self,
        get_dashboard_json,
        get_alert_json=None,
        save_wifi_profile=None,
        save_active_lanes=None
    ):
        self.get_dashboard_json = get_dashboard_json
        self.get_alert_json = get_alert_json
        self.save_wifi_profile = save_wifi_profile
        self.save_active_lanes = save_active_lanes
        self.portal_html = None

    def get_portal_html(self):
        if self.portal_html is None:
            with open("portal.html", "r") as f:
                self.portal_html = f.read()

        return self.portal_html

    async def handle_client(self, reader, writer):
        try:
            method, path, body = await read_request(reader)

            if method == "GET" and path == "/":
                response = http_response(
                    self.get_portal_html(),
                    content_type="text/html"
                )

            elif method == "GET" and path == "/api":
                response = http_response({
                    "message": "Pico Spool Monitor v2",
                    "dashboard": "/api/dashboard",
                    "alert": "/api/alert",
                    "health": "/api/health"
                })

            elif method == "GET" and path == "/api/health":
                response = http_response({
                    "ok": True
                })

            elif method == "GET" and path == "/api/dashboard":
                response = http_response(self.get_dashboard_json())

            elif method == "POST" and path == "/api/wifi/save":
                if self.save_wifi_profile is None:
                    response = http_response(
                        {"ok": False, "message": "wifi save unavailable"},
                        "501 Not Implemented"
                    )
                else:
                    try:
                        data = json.loads(body.decode() or "{}")
                        response = http_response(
                            self.save_wifi_profile(data)
                        )
                    except Exception as e:
                        response = http_response(
                            {"ok": False, "message": repr(e)},
                            "400 Bad Request"
                        )
            elif method == "GET" and path == "/api/alert":
                            if self.get_alert_json is None:
                                response = http_response(
                                    {"ok": False, "message": "alert endpoint unavailable"},
                                    "501 Not Implemented"
                                )
                            else:
                                response = http_response(self.get_alert_json()
                                )
            elif method == "POST" and path == "/api/active-lanes":
                if self.save_active_lanes is None:
                    response = http_response(
                        {"ok": False, "message": "active lane save unavailable"},
                        "501 Not Implemented"
                    )
                else:
                    try:
                        data = json.loads(body.decode() or "{}")
                        response = http_response(
                            self.save_active_lanes(data)
                        )
                    except Exception as e:
                        response = http_response(
                            {"ok": False, "message": repr(e)},
                            "400 Bad Request"
                        )

            else:
                response = http_response(
                    {"ok": False, "message": "not found"},
                    "404 Not Found"
                )

            await writer.awrite(response)

        except OSError:
            pass

        except Exception as e:
            try:
                await writer.awrite(
                    http_response(
                        {"ok": False, "message": repr(e)},
                        "500 Internal Server Error"
                    )
                )
            except Exception:
                pass

        finally:
            try:
                await writer.aclose()
            except Exception:
                pass

    async def start(self, port=80):
        return await asyncio.start_server(
            self.handle_client,
            "0.0.0.0",
            port
        )