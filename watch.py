import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Classe que vai lidar com os eventos
class MonitorArquivo(FileSystemEventHandler):
    def on_created(self, event):
        # Verifica se o arquivo foi criado e não é um diretório
        if not event.is_directory:
            print(f"Arquivo adicionado: {event.src_path}")
            
            # Conta o número de arquivos na pasta dados/input
            pasta_input = 'dados/input'
            total_arquivos = len([f for f in os.listdir(pasta_input) if os.path.isfile(os.path.join(pasta_input, f))])
            
            # Verifica se existem 3 arquivos na pasta
            if total_arquivos == 3:
                print(f"Existem 3 arquivos na pasta {pasta_input}. Executando o script.")
                # Executa o comando se houver 3 arquivos na pasta
                subprocess.run(["python", "processa.py"], shell=True)
            else:
                print(f"Existem {total_arquivos} arquivos na pasta {pasta_input}. Aguardando mais arquivos.")

# Função para iniciar a observação
def monitorar_pasta(caminho):
    event_handler = MonitorArquivo()
    observer = Observer()
    observer.schedule(event_handler, caminho, recursive=False)
    observer.start()
    print(f"Monitorando a pasta: {caminho}")

    try:
        while True:
            time.sleep(1)  # Espera enquanto monitora os eventos
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# Caminho da pasta a ser monitorada
pasta_para_monitorar = "./dados/input"

# Iniciar monitoramento
monitorar_pasta(pasta_para_monitorar)
