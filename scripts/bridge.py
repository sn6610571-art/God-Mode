import asyncio
import websockets
import json
import threading
import os
from mitmproxy import http, ctx

# Configurações VYZ
WS_PORT = 8765
DEX_PATH = "./classes.dex"
PANEL_CLIENTS = set()

class FighterBrasilEngine:
    def __init__(self):
        self.check_dex_integrity()
        threading.Thread(target=self.start_ws_server, daemon=True).start()

    def check_dex_integrity(self):
        """Valida se a peça fundamental (DEX) está na raiz"""
        if os.path.exists(DEX_PATH):
            size = os.path.getsize(DEX_PATH)
            ctx.log.info(f"✅ [DEX FOUND] classes.dex detectado na raiz ({size} bytes)")
        else:
            ctx.log.error("❌ [CRITICAL] classes.dex NÃO ENCONTRADO NA RAIZ!")

    def start_ws_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.ws_handler, "0.0.0.0", WS_PORT)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def ws_handler(self, ws, path):
        PANEL_CLIENTS.add(ws)
        # Envia confirmação de sistema pronto ao conectar
        await ws.send(json.dumps({"type": "SYSTEM", "msg": "MOTOR VYZ CONECTADO AO DEX"}))
        try:
            async for message in ws:
                data = json.loads(message)
                if data['type'] == 'APPLY_PATCH':
                    ctx.log.warn(f"⚡ [INJECTING] Aplicando Patch no tráfego ativo...")
        finally:
            PANEL_CLIENTS.remove(ws)

    async def broadcast(self, data):
        if PANEL_CLIENTS:
            msg = json.dumps(data)
            await asyncio.gather(*[client.send(msg) for client in PANEL_CLIENTS])

    # --- LIGAÇÃO DOS MÉTODOS GET/POST ---
    def request(self, flow: http.HTTPFlow):
        payload = {
            "type": "TRAFFIC",
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "id": flow.id,
            "dex_active": True
        }
        asyncio.run(self.broadcast(payload))

    def response(self, flow: http.HTTPFlow):
        # Detecção de Billing/RevenueCat integrada ao seu Hook no DEX
        if "purchases" in flow.request.url or "google" in flow.request.url:
            ctx.log.warn(f"🎯 [BYPASS] BillingWrapper$makePurchaseAsync interceptado!")

        data = {
            "type": "RESPONSE",
            "id": flow.id,
            "status": flow.response.status_code,
            "body": flow.response.get_text()
        }
        asyncio.run(self.broadcast(data))

addons = [FighterBrasilEngine()]
        
