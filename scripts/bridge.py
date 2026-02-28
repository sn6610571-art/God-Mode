from mitmproxy import http
import json

# Configuração: Onde o seu Dashboard v1000 salva as regras de ataque
RULES_PATH = "/sdcard/Download/res/rewrite_rules.json"

def request(flow: http.HTTPFlow):
    # 1. Detectar se o app está usando HMAC no Header
    if "X-HMAC-Signature" in flow.request.headers:
        print(f"[!] HMAC Detectado em: {flow.request.url}")
        # Aqui você poderia recalcular o hash se mudar o Body

def response(flow: http.HTTPFlow):
    # 2. Verificar se o domínio pertence ao seu site de teste
    if "seusite.com" in flow.request.pretty_host:
        
        try:
            # Tentar carregar as regras que você definiu no Dashboard HTML
            with open(RULES_PATH, "r") as f:
                rules = json.load(f)
            
            # 3. Aplicar o "Rewrite" (O dote que você queria)
            if rules.get("enabled"):
                data = flow.response.get_text()
                json_data = json.loads(data)
                
                # Exemplo: Se o Dashboard mandou mudar 'is_admin' para true
                for key, value in rules.get("modifications", {}).items():
                    json_data[key] = value
                
                # Devolve o JSON modificado para o App Alvo
                flow.response.set_text(json.dumps(json_data))
                flow.response.headers["X-Intercepted-By"] = "SecureLab-v1000"
                
                print(f"[SUCCESS] Payload modificado para {flow.request.path}")

        except Exception as e:
            print(f"[ERROR] Falha no Rewrite: {e}")

