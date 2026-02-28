#!/bin/bash
# setup_lab.sh - Versão Mobile (Executar via Termux no celular)

echo "🚀 Iniciando injeção via Termux..."

# O script vai procurar o APK na sua pasta de Downloads do celular
APK_LOCAL="/sdcard/Download/Reqable_sign.apk"

if [ -f "$APK_LOCAL" ]; then
    echo "📦 APK encontrado! Instalando..."
    adb install "$APK_LOCAL"
else
    echo "⚠️ Erro: Coloque o Reqable_sign.apk na pasta Download do celular"
fi

# Criar as pastas internas do app
echo "📂 Criando pastas de sistema..."
adb shell "su -c 'mkdir -p /data/data/com.reqable.android/files/reqable/res'"

# Enviar os scripts que você criou no GitHub
echo "🌉 Enviando Bridge e Configurações..."
adb push scripts/bridge.py /sdcard/Download/
adb shell "su -c 'mv /sdcard/Download/bridge.py /data/data/com.reqable.android/files/reqable/res/'"

echo "✅ Pronto! O motor v1000 foi injetado."
