from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from log import logger

# Configurar a pasta de download
download_dir = "D:\\Dev\\DataScience\\vestibular\\dados\\input"

# Configura as opções do Chrome para definir a pasta de download
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # Diretório onde o arquivo será salvo
    "download.prompt_for_download": False,  # Baixar automaticamente sem perguntar
    "download.directory_upgrade": True,  # Atualiza o diretório
    "safebrowsing.enabled": True  # Evitar alertas de segurança de navegação
}
chrome_options.add_experimental_option("prefs", prefs)

# Configurando o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)


url = "https://concurso3.fundacaocefetminas.org.br/cliente/resumo_inscricoes.aspx"
# Acessa a página de login
driver.get(url)

driver.maximize_window()

# Preenche o campo de login
username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtEmail")))
if (username_input.is_displayed()):
    username_input.send_keys("49097067634")

# Preenche o campo de senha
password_input = driver.find_element(By.ID, "txtSenha")
if(password_input.is_displayed()):
    password_input.send_keys("IFMG2024*")

# Clica no botão de login
login_button = driver.find_element(By.ID, "cmdEntrar")
if(login_button.is_displayed()):
    login_button.click()


driver.get(url)
time.sleep(5)

# Seleciona o campo select e extrai as opções
try:
    # Espera o dropdown ficar visível
    # print("Esperando o dropdown ficar visível")
    select_element = driver.find_element(By.ID, "ContentPlaceHolder1_dropProcesso")
    
    # Extrai todas as opções do dropdown
    options = select_element.find_elements(By.TAG_NAME, "option")
    
    for option in options:
        option.click()
        time.sleep(1)  
        value = option.get_attribute("value")
        if value in [ "106", "107", "108"]:
            text = option.get_attribute("text")
            driver.find_element(By.ID, "ContentPlaceHolder1_cmdGerar").click()
            logger.info(f"Baixando arquivo {text}...")
            time.sleep(2)
    
except Exception as e:
    print(f"Erro ao selecionar o campo ou processar as opções: {e}")
    logger.error(f"Erro ao selecionar o campo ou processar as opções: {e}") 

# Fecha o navegador após completar o processo
driver.quit()
