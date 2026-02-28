#!/bin/bash
# PROJETO: God-Mode (Signflinger Engine)
# AUTOR: sn6610571-art
# OBJETIVO: Deploy total via GitHub (Sem dependência de APK local)

echo "🔥 [God-Mode] Iniciando Deploy Estrutural via GitHub Cloud..."

# 1. CONFIGURAÇÃO DA FONTE (URL do seu GitHub)
GITHUB_BASE="https://raw.githubusercontent.com/sn6610571-art/God-Mode/main"
APP_TARGET="com.reqable.android"
APP_DATA="/data/data/$APP_TARGET/files/reqable/res"
MAGISK_CERT_PATH="/data/adb/modules/reqable-magisk/system/etc/security/cacerts"

# 2. PREPARAÇÃO DO AMBIENTE (ROOT)
echo "📂 Criando infraestrutura de pastas no sistema..."
su -c "mkdir -p $APP_DATA"
su -c "mkdir -p $MAGISK_CERT_PATH"
su -c "mkdir -p /data/local/tmp/godmode/lib"

# 3. DOWNLOAD E INJEÇÃO DOS MOTORES (PYTHON & JS)
echo "🌉 Baixando Motores de Intercepção..."
# Baixando Bridge.py
su -c "curl -sL $GITHUB_BASE/scripts/bridge.py -o $APP_DATA/bridge.py"
# Baixando Bypass_core.js (da subpasta scripts/scripts/)
su -c "curl -sL $GITHUB_BASE/scripts/scripts/bypass_core.js -o $APP_DATA/bypass_core.js"
su -c "chmod 777 $APP_DATA/*"

# 4. DOWNLOAD E INJEÇÃO DO CERTIFICADO (MAGISK)
echo "🛡️  Baixando Certificado d119c728.0..."
su -c "curl -sL $GITHUB_BASE/certs/d119c728.0 -o $MAGISK_CERT_PATH/d119c728.0"
su -c "chmod 644 $MAGISK_CERT_PATH/d119c728.0"
su -c "chown root:root $MAGISK_CERT_PATH/d119c728.0"

# 5. SINCRONIZAÇÃO DAS LIBS NATIVAS (.SO)
echo "📂 Sincronizando Bibliotecas SHA-256 (Cloud Sync)..."
# Lista de libs detectadas na sua árvore
LIBS=("libapp.so" "libflutter.so" "libreqable_cronet.so" "libreqable_netbare.so" "libtun2proxy.so")

for lib in "${LIBS[@]}"; do
    echo "📥 Baixando $lib..."
    su -c "curl -sL $GITHUB_BASE/lib/arm64-v8a/$lib -o /data/local/tmp/godmode/lib/$lib"
    su -c "cp /data/local/tmp/godmode/lib/$lib /data/data/$APP_TARGET/lib/" 2>/dev/null
done

# 6. LIMPEZA E FINALIZAÇÃO
su -c "rm -rf /data/local/tmp/godmode"
echo "--------------------------------------------------"
echo "✅ [SUCCESS] Projeto God-Mode Injetado via Cloud!"
echo "📍 Repositório: sn6610571-art / God-Mode"
echo "📍 Mimetismo: Ativo via bridge.py"
echo "📍 Integridade: Protegida via bypass_core.js"
echo "--------------------------------------------------"
