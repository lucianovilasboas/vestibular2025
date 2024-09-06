import pandas as pd
import os
from datetime import datetime
import shutil 
from funcoes import process_file_for_subsequente, process_file_for_integrado, process_file_for_superior
from log import logger

if __name__ == "__main__":
    
    # Define os caminhos das pastas
    dados_folder = "./dados"
    input_folder = "./dados/input"
    processed_folder = "./dados/processed"
    backup_folder = "./dados/backup"
    name_ext = ""
    timestamp = datetime.now()
    # Gera o novo nome para o arquivo com base na data de leitura
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")

    # Tenta listar todos os arquivos na pasta de entrada
    try:
        files = os.listdir(input_folder)
        if not files:
            print(f"{timestamp_str} - Nenhum arquivo encontrado na pasta input.")
            logger.warn(f"Nenhum arquivo encontrado na pasta input.")
            exit()
    except Exception as e:
        print(f"{timestamp_str} - Nenhum arquivo encontrado na pasta input.")
        logger.warn(f"Nenhum arquivo encontrado na pasta input - {e}")
        exit()

    # lendo o dataframe final
    df_all = pd.read_excel("./dados/processed/all_data.xlsx")
    dataframes = [df_all]
    for file in files:
        if file.endswith('.xlsx'):
            # Define o caminho completo do arquivo
            file_path = os.path.join(input_folder, file)
            
            # Lê o arquivo Excel
            df = pd.read_excel(file_path)
            # ler a primeira linha do dataframe e verificar se é um arquivo de graduação, integrado ou subsequente
            # para isso use a coluna "Processo" conforme abaixo:
            # IFMG - Processo Seletivo Cursos Graduação 2025/1             -> Graduação
            # IFMG - Processo Seletivo Cursos Técnicos Integrados 2025/1   -> Integrado
            # IFMG - Processo Seletivo Cursos Técnicos Subsequentes 2025/1 -> Subsequente 
            first_row = df.iloc[0] # pega a primeira linha do dataframe
            if "Graduação" in first_row["Processo"]:
                df = process_file_for_superior(file_path)
                name_ext = "Superior"
            elif "Integrados" in first_row["Processo"]:
                df = process_file_for_integrado(file_path)
                name_ext = "Integrado"
            elif "Subsequentes" in first_row["Processo"]:
                df = process_file_for_subsequente(file_path)
                name_ext = "Subsequente"
            else:
                print(f"{timestamp_str} - Arquivo {file} não foi processado. Formato não reconhecido.")
                logger.warn(f"Arquivo {file} não foi processado. Formato não reconhecido.")
                continue
            
            # Registra o timestamp da leitura
            df['Timestamp'] = timestamp
            
            dataframes.append(df)
            
            file_name = f"{os.path.splitext(file)[0]}"
            new_file_name = f"{file_name}_{name_ext}_{timestamp_str}.xlsx"
            new_file_path = os.path.join(processed_folder, new_file_name)  
            
            # Copia o arquivo para a pasta backup
            shutil.copy(file_path, os.path.join(backup_folder, new_file_name))
            # Copia o arquivo para a pasta dados e renomeia para 
            # 2025-1_GestaoResultado_ResumoInscricoes_X.xlsx
            # com X sendo "GRAD", "TEC" ou "SUB" dependendo do tipo de curso na variavel name_ext
            shutil.copy(file_path, os.path.join(dados_folder, f"2025-1_GestaoResultado_ResumoInscricoes_{name_ext}.xlsx"))

            # Move e renomeia o arquivo para a pasta processados
            shutil.move(file_path, new_file_path)
            
            print(f"{timestamp_str} - Arquivo {file} processado e movido para {new_file_path}")
            logger.info(f"Arquivo {file} processado e movido para {new_file_path}")

    csv_file_path = os.path.join(processed_folder, "all_data")
    df_all = pd.concat(dataframes)
    df_all.to_csv(f"{csv_file_path}.csv", index=False, encoding="latin1")
    df_all.to_excel(f"{csv_file_path}.xlsx", index=False)

    print(f"{timestamp_str} - Todos os arquivos processados e movidos com sucesso!")
    logger.info(f"Todos os arquivos processados e movidos com sucesso!")