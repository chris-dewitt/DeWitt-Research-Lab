"""Minimal public-fixture HTTP adapter for local and Cloud Run prototypes."""

from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from drl_protocol import TaskRequest

from .runtime import build_local_runtime

MAX_BODY_BYTES = 64 * 1024


class AtticusHandler(BaseHTTPRequestHandler):
    """Expose health and bounded public task endpoints without content logs."""

    server_version = "AtticusFoundation/0.1"

    def log_message(self, format: str, *args: object) -> None:
        # Avoid logging user objectives in the foundation server.
        return

    def _send(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._send(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "service": "atticus-control-plane",
                    "maturity": "prototype",
                },
            )
            return
        self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/tasks":
            self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_content_length"})
            return
        if length <= 0 or length > MAX_BODY_BYTES:
            self._send(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "invalid_body_size"})
            return
        try:
            payload = json.loads(self.rfile.read(length))
            objective = str(payload["objective"]).strip()
            if not objective or len(objective) > 8_000:
                raise ValueError("objective must contain 1 to 8000 characters")
            as_of = str(payload.get("as_of", "2026-07-24"))
            task_id = str(payload.get("task_id", "public-http-task"))[:128]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)})
            return

        request = TaskRequest(
            task_id=task_id,
            objective=objective,
            session_id="public-http",
            actor_id="anonymous",
            public_session=True,
            as_of=as_of,
        )
        try:
            result = build_local_runtime().run(request)
        except ValueError as exc:
            self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)})
            return
        self._send(HTTPStatus.OK, result.to_dict())


def main() -> int:
    host = os.environ.get("ATTICUS_HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer((host, port), AtticusHandler)
    print(f"Atticus foundation server listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
