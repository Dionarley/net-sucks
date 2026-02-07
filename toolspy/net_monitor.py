import os
import time
import subprocess

def check_internet():
    # Tenta pingar o DNS do Google. 
    # -c 1: apenas um pacote
    # -W 2: espera no máximo 2 segundos por resposta
    status = os.system("ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1")
    return status == 0

def send_notification():
    title = "Conexão Restabelecida"
    msg = "O Arch Linux está online novamente!"
    # 'notify-send' funciona na maioria das DEs (GNOME, KDE, XFCE, i3, etc)
    os.system(f'notify-send "{title}" "{msg}" --icon=network-wired')

def main():
    print("[-] Monitorando... O script avisará quando a rede voltar.")
    
    was_offline = True # Assume que começou offline para disparar o aviso
    
    while True:
        if check_internet():
            if was_offline:
                print("[+] Conectado!")
                send_notification()
                # Se quiser que o script pare ao conectar, use 'break'
                # Se quiser que ele continue monitorando, mude a flag:
                was_offline = False
        else:
            if not was_offline:
                print("[!] A conexão caiu...")  
                was_offline = True
        
        time.sleep(60) 

if __name__ == "__main__":
    main()
