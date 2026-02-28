#!/bin/bash
# setup_lab.sh — O Injetor do SecureLab v1000

echo "🚀 Iniciando Injeção de Recursos no Dispositivo..."

# 1. Definir o nome do pacote do seu APK (ajuste se necessário)
PACKAGE_NAME="com.reqable.android" 
TARGET_DIR="/data/data/$PACKAGE_NAME/files/reqable"

# 2. Criar a estrutura de pastas originais (O que o .so procura)
adb shell "su -c 'mkdir -p $TARGET_DIR/res $TARGET_DIR/cert $TARGET_DIR/scripts'"

# 3. Enviar o motor Python e o Mapa de Versão
echo "📦 Enviando Motores de Scripting..."
adb push resources/overrides-python.zip /sdcard/Download/
adb push resources/overrides-version.json /sdcard/Download/
adb shell "su -c 'mv /sdcard/Download/overrides-* $TARGET_DIR/res/'"

# 4. Enviar o Certificado para o Magisk (Bypass de SSL Pinning na raiz)
echo "🔐 Injetando Certificado CA..."
adb push certs/reqable_ca.crt /sdcard/Download/
# O módulo Magisk vai ler deste caminho para mover para /system/etc/security/cacerts/

# 5. Enviar o Script Bridge (O motor de Rewrite)
echo "🌉 Ativando a Ponte de Interceptação..."
adb push scripts/bridge.py /sdcard/Download/
adb shell "su -c 'mv /sdcard/Download/bridge.py $TARGET_DIR/scripts/'"

# 6. Permissões de Execução (O segredo para não dar erro de I/O)
adb shell "su -c 'chmod -R 777 $TARGET_DIR'"

echo "✅ Sistema pronto! Reinicie o celular para o Magisk ativar o Certificado."

