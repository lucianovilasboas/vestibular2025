import schedule
import subprocess
import time
from log import logger

# Função para executar os scripts
def executar():
    print("Executando agenda.py...")
    print("  Executando automacao.py...")
    logger.info("Executando automacao.py...")
    subprocess.run(["python", "automacao.py"], shell=True)
    logger.info("Execução finalizada.")

    print("  Executando processa.py...")
    logger.info("Executando processa.py...")
    subprocess.run(["python", "processa.py"], shell=True)
    logger.info("Execução finalizada.")

    print("  Executando gitrun.py...")
    logger.info("Executando gitrun.py...")
    subprocess.run(["python", "gitrun.py", "-m", "Data update using git"], shell=True)
    logger.info("Execução finalizada.")

    print("Finalizando execução da agenda.py")


if __name__ == "__main__":
    logger.info("Iniciando agendamento...")
    agendamentos = ["07:00", "12:00", "18:00" ,"22:00"] 
    for i, a in enumerate(agendamentos):
        text = f"{i+1}° agendamento para {a}"
        print(text)
        logger.info(text)
        # Agendar as tarefas
        schedule.every().day.at(a).do(executar)

    # Loop para manter o agendador rodando
    while True:
        schedule.run_pending()  # Executa tarefas agendadas
        time.sleep(10)  # Pausa para evitar alto consumo de CPU
    
    logger.info("Agendamento finalizado.")
