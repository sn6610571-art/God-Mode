// bypass_core.js
Java.perform(function() {
    // 1. Bypass Anti-Debug (Impede o app de fechar ao detectar o Frida)
    var Debug = Java.use('android.os.Debug');
    Debug.isDebuggerConnected.implementation = function() {
        return false; 
    };

    // 2. Bypass Detecção de Proxy (Faz o app achar que a rede é direta)
    var NetworkCapabilities = Java.use('android.net.NetworkCapabilities');
    NetworkCapabilities.hasCapability.implementation = function(cap) {
        if (cap == 11) return true; // NET_CAPABILITY_NOT_METERED
        return this.hasCapability(cap);
    };

    // 3. Forçar aceitação do Certificado User (mesmo com HSTS)
    var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
    TrustManagerImpl.checkServerTrusted.implementation = function(chain, authType, host) {
        return chain; // Aceita qualquer certificado injetado
    };

    console.log("🛡️ [SecureLab] Camadas de segurança neutralizadas!");
});

