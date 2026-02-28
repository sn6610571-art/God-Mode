import asyncio
import websockets
import json
import os
import threading
from mitmproxy import http, ctx
from mitmproxy import http, ctx, websocket
import json
import os
import time
import asyncio
# import websockets # Para comunicação com o seu Painel HTML
# import schema_pb2 # Suas classes Protobuf compiladas

# --- NOVA ÁRVORE GOD-MODE (100% ROOT/SISTEMA) ---
APP_DATA_PATH = "/data/data/com.reqable.android/files/reqable/res"
RULES_PATH = f"{APP_DATA_PATH}/rewrite_rules.json"
SUFFIX_PATH = f"{APP_DATA_PATH}/publicsuffixes/publicsuffixes.gz"
LIB_PATH = "/data/data/com.reqable.android/lib" 

class GodModeEngine:
    def __init__(self):
        self.premium_headers = {
            "date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
            "content-type": "application/json; charset=utf-8",
            "access-control-allow-origin": "https://betnacional.bet.br",
            "cf-cache-status": "DYNAMIC",
            "server": "cloudflare",
            "cf-ray": "9d24d3694a30f638-FOR",
            "alt-svc": 'h3=":443"; ma=86400'
        }
        self.check_tree_integrity()

    def check_tree_integrity(self):
        """Verifica se a nova árvore foi injetada pelo setup_lab.sh"""
        if os.path.exists(LIB_PATH):
            ctx.log.info(f"📂 [TREE] Bibliotecas Nativas Mapeadas em {LIB_PATH}")
        if os.path.exists(SUFFIX_PATH):
            ctx.log.info("🌐 [TREE] Regras OkHttp PublicSuffix Carregadas!")

    # --- 1. INTERCEPÇÃO DE REQUISIÇÃO (MIMETISMO) ---
    def request(self, flow: http.HTTPFlow):
        # Enganando o servidor para achar que somos o Flutter/Dart Original
        flow.request.headers["User-Agent"] = "Dart/3.0 (dart:io)"
        flow.request.headers["X-Requested-With"] = "com.betnacional.app"

        # Bypass de Assinatura via Headers
        if "X-HMAC-Signature" in flow.request.headers:
            ctx.log.warn(f"⚡ [BYPASS] Assinatura Detectada: {flow.request.headers['X-HMAC-Signature'][:15]}...")

    # --- 2. INTERCEPÇÃO DE RESPOSTA (REWRITE & PROTOBUF) ---
    def response(self, flow: http.HTTPFlow):
        targets = ["betnacional.bet.br", "api.seusite.com"]
        
        if any(t in flow.request.pretty_host for t in targets):
            ctx.log.info(f"🎯 [GOD-MODE] Alvo Interceptado: {flow.request.pretty_url}")

            # Mimetismo Cloudflare
            for key, value in self.premium_headers.items():
                flow.response.headers[key] = value

            # Anti-Cache
            flow.response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

            content_type = flow.response.headers.get("Content-Type", "")

            # --- MOTOR DE REWRITE DINÂMICO ---
            try:
                # 2.1. Processamento de PROTOBUF (Binário)
                if "application/x-protobuf" in content_type or "application/grpc" in content_type:
                    ctx.log.warn("📦 [PROTOBUF DETECTADO] Iniciando descompactação binária...")
                    # Exemplo de como o motor aplica o Line Patch no Protobuf:
                    # data = schema_pb2.ResponsePayload()
                    # data.ParseFromString(flow.response.content)
                    # if data.balance: 
                    #     data.balance = 999999.99  # O Line Patch do HTML
                    # flow.response.content = data.SerializeToString()
                    # ctx.log.info("✅ Protobuf modificado e re-empacotado!")

                # 2.2. Processamento de JSON
                elif "application/json" in content_type:
                    if os.path.exists(RULES_PATH):
                        with open(RULES_PATH, "r") as f:
                            rules = json.load(f)
                        
                        if rules.get("enabled"):
                            data = json.loads(flow.response.content)
                            for key, value in rules.get("modifications", {}).items():
                                if key in data:
                                    data[key] = value
                                    ctx.log.info(f"💎 [PATCH] {key} -> {value}")
                            
                            flow.response.content = json.dumps(data).encode("utf-8")
            except Exception as e:
                ctx.log.error(f"❌ [FALHA NO REWRITE]: {e}")

    # --- 3. INTERCEPÇÃO DE WEBSOCKETS (LIVE STREAM) ---
    def websocket_message(self, flow: websocket.WebSocketFlow):
        message = flow.messages[-1]
        direcao = "CLIENT -> SERVER" if message.from_client else "SERVER -> CLIENT"
        
        if message.is_text:
            ctx.log.info(f"🌐 [WS TEXT] {direcao}: {message.content[:50]}")
        else:
            ctx.log.warn(f"📦 [WS BINARY/PROTO] {direcao}: {len(message.content)} bytes")
            # Aqui o motor converte o binário e manda pro seu index.html
            
        # self.broadcast_to_ui(flow) # Envia para o Painel

addons = [GodModeEngine()]


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
