import asyncio
import websockets
import json
import os
import threading
from mitmproxy import http, ctx

# Configurações VYZ
WS_HOST = "0.0.0.0"
WS_PORT = 8765
DEX_FILE = "./classes.dex"
PANEL_CLIENTS = set()

class VyzFighterEngine:
    def __init__(self):
        self.check_dex()
        threading.Thread(target=self.start_ws_server, daemon=True).start()

    def check_dex(self):
        if os.path.exists(DEX_FILE):
            ctx.log.info(f"✅ [SYSTEM] classes.dex vinculado! Proteções desativadas.")
        else:
            ctx.log.error("❌ [CRITICAL] classes.dex não encontrado na raiz!")

    def start_ws_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.ws_handler, WS_HOST, WS_PORT)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def ws_handler(self, ws, path):
        PANEL_CLIENTS.add(ws)
        try:
            async for message in ws:
                data = json.loads(message)
                if data["type"] == "PATCH_APPLY":
                    # Aqui você salvaria a regra para aplicar no próximo flow
                    ctx.log.warn(f"⚡ [REWRITE] Novo Patch recebido para URL: {data['url']}")
        finally:
            PANEL_CLIENTS.remove(ws)

    async def broadcast(self, data):
        if PANEL_CLIENTS:
            msg = json.dumps(data)
            await asyncio.gather(*[client.send(msg) for client in PANEL_CLIENTS])

    # Interceptação de Fluxo
    def request(self, flow: http.HTTPFlow):
        req_data = {
            "type": "TRAFFIC",
            "id": flow.id,
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "headers": dict(flow.request.headers),
            "size": len(flow.request.content)
        }
        asyncio.run(self.broadcast(req_data))

    def response(self, flow: http.HTTPFlow):
        res_data = {
            "type": "RESPONSE",
            "id": flow.id,
            "status": flow.response.status_code,
            "body": flow.response.get_text(),
            "headers": dict(flow.response.headers)
        }
        asyncio.run(self.broadcast(res_data))

addons = [VyzFighterEngine()]
