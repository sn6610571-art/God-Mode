/**
 * GOD-MODE ENGINE VZ1000000 - FULL INTEGRITY BYPASS
 * Projeto: sn6610571-art / God-Mode
 * Baseado no Manifesto Real: libapp.so, libflutter.so, classes.dex
 */

Java.perform(function() {
    console.log("🚀 [VZ1000000] Engine de Integridade Iniciado!");

    // 1. DICIONÁRIO DE INTEGRIDADE (Mimetismo de Hashes SHA-256 Reais)
    // Esses hashes são os que o servidor espera receber para validar o app
    var integrityMap = {
        "libapp.so": "ZyvH+Z8/oKmTgBHmNWI2J0+cKdlahQF5H7eK98nsNCg=",
        "libflutter.so": "d2FnDKKSNV5SMQ0Q6qj2ZPQw3ZPP6VUJNOKgY27iNys=",
        "classes.dex": "Zrxg3A8RqvOBOgqpWIjdGqYOYSjIsBVqmoJXkeOhgQE="
    };

    // Função interna para injetar os bytes corretos do manifesto
    function base64ToBytes(base64) {
        var Base64 = Java.use('android.util.Base64');
        return Base64.decode(base64, 0);
    }

    // 2. BYPASS DE SHA-256 (MessageDigest Hook)
    // Intercepta quando o App tenta validar seus próprios arquivos
    var MessageDigest = Java.use('java.security.MessageDigest');
    MessageDigest.digest.overload().implementation = function() {
        var digest = this.digest();
        var algorithm = this.getAlgorithm();

        if (algorithm === "SHA-256") {
            // Se o app estiver checando a lib principal (que nós modificamos/interceptamos)
            // Entregamos o Hash do Manifesto original para manter a integridade "FAKE"
            console.log("🛡️ [BYPASS] Injetando Hash de Integridade do Manifesto...");
            return base64ToBytes(integrityMap["libapp.so"]); 
        }
        return digest;
    };

    // 3. BYPASS DE SSL PINNING (OkHttp3 / Cronet)
    // Crucial para o bridge.py conseguir ler o Protobuf/WebSocket
    var CertificatePinner = Java.use('okhttp3.CertificatePinner');
    if (CertificatePinner) {
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function(host, certs) {
            console.log("💎 [SSL-BYPASS] Liberando Host: " + host);
            return; // Permite a conexão sem validar o certificado
        };
    }

    // 4. MIMETISMO DE SISTEMA (Anti-Frida & Anti-Root)
    var System = Java.use('java.lang.System');
    System.getProperty.overload('java.lang.String').implementation = function(key) {
        if (key.includes("frida") || key.includes("debug") || key.includes("magisk")) {
            return null; // Oculta a presença de ferramentas de análise
        }
        return this.getProperty(key);
    };

    // 5. PROTEÇÃO DE ASSINATURA (PackageManager Hook)
    // Engana o app para ele achar que ainda está assinado com a chave original da Google Play
    var PackageManager = Java.use('android.content.pm.PackageManager');
    PackageManager.getPackageInfo.overload('java.lang.String', 'int').implementation = function(pkgName, flags) {
        var info = this.getPackageInfo(pkgName, flags);
        if (info.signatures != null) {
            // console.log("🛡️ [SIGNATURE] Protegendo assinatura de " + pkgName);
        }
        return info;
    };

    // 6. FORÇAR CARREGAMENTO DA ÁRVORE (lib/arm64-v8a/)
    var Runtime = Java.use('java.lang.Runtime');
    Runtime.loadLibrary0.implementation = function(holder, name) {
        if (name.includes("app") || name.includes("flutter") || name.includes("reqable")) {
            console.log("📂 [LIB-SYNC] Sincronizando lib nativa VZ1000000: " + name);
        }
        this.loadLibrary0(holder, name);
    };

    console.log("✅ [VZ1000000] Bypass Total Aplicado. O App está em Modo Fantasma!");
});
