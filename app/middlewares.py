import time
from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send

class ResponseTimeMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()

        async def _send(message: dict) -> None:
            if message["type"] == "http.response.start":
                response_headers = message.get("headers", [])
                response_headers.append((b"X-Response-Time", str(time.time() - start_time).encode()))
                message["headers"] = response_headers
            await send(message)

        await self.app(scope, receive, _send)


