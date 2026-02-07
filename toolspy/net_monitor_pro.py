import os
import time
from datetime import datetime

# --- CONFIGURAÇÕES ---
ALVO_PING = "1.1.1.1"    # IP estável (Cloudflare)
INTERVALO = 2            # Verificação a cada 2 segundos
LOG_FILE = "historico_conexao.txt"

def check_internet():
    """Verifica a conectividade via comando ping."""
    # -c 1 (1 pacote), -W 1 (espera 1 seg)
    status = os.system(f"ping -c 1 -W 1 {ALVO_PING} > /dev/null 2>&1")
    return status == 0

def enviar_notificacao(titulo, mensagem, icone, urgencia="normal"):
    """Dispara o pop-up no desktop usando libnotify."""
    os.system(f'notify-send "{titulo}" "{mensagem}" -i {icone} -u {urgencia}')

def registrar_evento(tipo, duracao=None):
    """Escreve no arquivo de log com timestamp."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        if tipo == "QUEDA":
            f.write(f"[{agora}] ❌ QUEDA DETECTADA\n")
        elif tipo == "VOLTA":
            f.write(f"[{agora}] ✅ CONECTADO (Tempo offline: {duracao})\n")
            f.write("-" * 45 + "\n")

def main():
    online = True
    inicio_queda = None

    print(f"--- 🛰️  Monitor de Rede Ativo ---")
    print(f"Salvando logs em: {os.path.abspath(LOG_FILE)}")
    
    try:
        while True:
            conectado = check_internet()

            # Transição: Estava ONLINE e agora está OFFLINE
            if online and not conectado:
                online = False
                inicio_queda = time.time()
                
                enviar_notificacao("Rede Indisponível", "Sua internet caiu!", "network-error", "critical")
                registrar_evento("QUEDA")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Conexão perdida...")

            # Transição: Estava OFFLINE e agora está ONLINE
            elif not online and conectado:
                online = True
                segundos_fora = int(time.time() - inicio_queda)
                
                # Formatação amigável do tempo
                m, s = divmod(segundos_fora, 60)
                tempo_str = f"{m}m {s}s" if m > 0 else f"{s}s"
                
                enviar_notificacao("Rede Restaurada", f"Ficou offline por {tempo_str}", "network-transmit-receive")
                registrar_evento("VOLTA", tempo_str)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Conexão restabelecida! ({tempo_str})")

            time.sleep(INTERVALO)
            
    except KeyboardInterrupt:
        print("\n[!] Monitoramento parado pelo usuário.")

if __name__ == "__main__":
    main()
