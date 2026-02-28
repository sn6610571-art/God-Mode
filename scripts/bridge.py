from mitmproxy import http
import json
import os
import time
import subprocess

# --- MAPEAMENTO DINÂMICO DA ÁRVORE GOD-MODE ---
BASE_PATH = "/data/adb/modules/reqable-magisk"
RULES_PATH = "/sdcard/Download/res/rewrite_rules.json"
CERT_HASH = "d119c728.0"
LIB_PATH = f"{BASE_PATH}/system/lib64" # Onde as .so residem

class GodModeEngine:
    def __init__(self):
        self.premium_headers = {
            "date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
            "content-type": "application/json; charset=utf-8",
            "access-control-allow-credentials": "true",
            "access-control-allow-origin": "https://betnacional.bet.br",
            "vary": "Origin",
            "content-security-policy": "frame-ancestors com.br;",
            "x-frame-options": "deny",
            "x-xss-protection": "1; mode=block",
            "x-content-type-options": "nosniff",
            "cf-cache-status": "DYNAMIC",
            "server": "cloudflare",
            "cf-ray": "9d24d3694a30f638-FOR",
            "alt-svc": 'h3=":443"; ma=86400'
        }
        self.check_system_integrity()

    def check_system_integrity(self):
        """Verifica se o Magisk injetou o certificado corretamente (Root Check)"""
        system_cert = f"/system/etc/security/cacerts/{CERT_HASH}"
        if os.path.exists(system_cert):
            print(f"🛡️ [INTEGRITY] Certificado {CERT_HASH} detectado no Sistema!")
        else:
            print(f"⚠️ [WARNING] Certificado não encontrado no path de sistema. Verifique o service.sh.")

    def request(self, flow: http.HTTPFlow):
        # 1. MIMETISMO DE APP ORIGINAL (Bypass de detecção de Bot)
        flow.request.headers["User-Agent"] = "Dart/3.0 (dart:io)"
        flow.request.headers["X-Requested-With"] = "com.betnacional.app"
        
        # 2. BYPASS DE ASSINATURA (Integrando com a Lib nativa se necessário)
        if "X-HMAC-Signature" in flow.request.headers:
            # Aqui o motor poderia chamar a libapp.so da sua árvore para validar o hash
            print(f"⚡ [BYPASS] HMAC Session: {flow.request.headers.get('X-HMAC-Signature')[:16]}...")

    def response(self, flow: http.HTTPFlow):
        # 3. ALVOS UNIVERSAIS
        targets = ["betnacional.bet.br", "api.seusite.com"]
        
        if any(t in flow.request.pretty_host for t in targets):
            print(f"🎯 [GOD-MODE] Interceptando Alvo: {flow.request.pretty_host}")

            # 4. INJEÇÃO DE CABEÇALHOS (Unificação Total Cloudflare)
            for key, value in self.premium_headers.items():
                flow.response.headers[key] = value

            # 5. MOTOR DE REWRITE (Sincronizado com o Dashboard HTML)
            try:
                if os.path.exists(RULES_PATH):
                    with open(RULES_PATH, "r") as f:
                        rules = json.load(f)
                    
                    if rules.get("enabled"):
                        data = flow.response.json()
                        modifications = rules.get("modifications", {})
                        
                        # Loop de Modificação Profissional
                        for key, value in modifications.items():
                            if key in data:
                                data[key] = value
                                print(f"💎 [MOD] {key} -> {value}")
                        
                        flow.response.set_text(json.dumps(data))

                # 6. BYPASS DE HSTS/CACHE (Anti-Detecção)
                flow.response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                flow.response.headers["Expires"] = "0"

            except Exception as e:
                print(f"❌ [CRITICAL] Erro no processamento do payload: {e}")

addons = [GodModeEngine()]
    
