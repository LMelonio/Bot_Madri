from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
import os
import time

# Diretório onde o script está localizado
download_dir = r'C:\Users\MADRI EXPRESS\Desktop\aut_madri'

# Configurar as opções do Chrome para definir o diretório de download e modo headless
def configurar_navegador(download_dir):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': download_dir}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--headless')  # Manter headless ativado
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=chrome_options)

# Acessar e logar no site
def login(driver, wait):
    print("Iniciando login...")
    driver.get("http://18.229.49.54/jadexpress/index.php")
    cidade_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "idlocal")))
    Select(cidade_dropdown).select_by_visible_text("SAO LUIZ-MA")
    
    username = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/form/div[2]/input")))
    password = wait.until(EC.presence_of_element_located((By.ID, "senha")))
    password.clear()
    username.send_keys("cutrim")
    time.sleep(2)
    password.send_keys("thiago123")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/form/div[4]/input")))
    login_button.click()
    time.sleep(3)
    print("Login - concluído.")

# Acessar a página de relatórios e preencher datas
def acessar_relatorio_e_preencher_datas(driver, wait):
    print("Acessando relatório e preenchendo datas...")
    driver.get("http://18.229.49.54/jadexpress/financeiro/frete/relatorioConhecimento.php")
    time.sleep(2)
    
    data_inicial = (datetime.now() - timedelta(days=1)).strftime("%d%m%Y")
    data_final = datetime.now().strftime("%d%m%Y")
    
    data_inicial_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/form/center/div/table[1]/tbody/tr/td[1]/input')))
    data_final_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/form/center/div/table[1]/tbody/tr/td[3]/input')))
    data_inicial_input.clear()
    data_inicial_input.send_keys(data_inicial)
    data_final_input.clear()
    data_final_input.send_keys(data_final)
    print("Datas preenchidas - concluído.")

# Selecionar opções do relatório
def selecionar_opcoes_relatorio(driver, wait):
    print("Selecionando opções do relatório...")
    try:
        opcoes_xpath = [
            '//*[@id="c_emitente"]', '//*[@id="c_dataemissao"]', '//*[@id="c_horaemissao"]',
            '//*[@id="c_tomador"]', '//*[@id="c_cidadeUfRem"]', '//*[@id="c_destinatario"]',
            '//*[@id="c_cidadeUfDest"]', '//*[@id="c_volume"]', '//*[@id="c_manifesto"]',
            '//*[@id="c_motivo"]', '//*[@id="c_dataprevista"]', '//*[@id="c_dataentrega"]',
            '//*[@id="c_statusrastreio"]'
        ]
        for xpath in opcoes_xpath:
            # Esperar até que o elemento seja visível e clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
    except Exception as e:
        print(f"Erro ao selecionar opções do relatório: {e}")
    else:
        print("Opções do relatório selecionadas.")

# Buscar relatório e baixar CSV
def baixar_csv(driver, wait, download_dir):
    print("Buscando relatório e baixando CSV...")
    try:
        button_buscar = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/form/center/div/table[3]/tbody/tr/td[17]/input')
        button_buscar.click()
        csv_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="meu_form2_wrapper"]/div[1]/div/a[2]')))
        csv_button.click()
        time.sleep(5)
        
        # Verificar se o arquivo anterior existe e excluir
        old_csv_file = os.path.join(download_dir, 'relatorio_scorpius.csv')
        if os.path.exists(old_csv_file):
            os.remove(old_csv_file)

        # Verificar se o novo arquivo CSV foi baixado e renomeá-lo
        for file in os.listdir(download_dir):
            if file.endswith('.csv'):
                new_csv_file_path = os.path.join(download_dir, file)
                os.rename(new_csv_file_path, old_csv_file)
                break
    except Exception as e:
        print(f"Erro ao baixar o CSV: {e}")
    else:
        print("CSV baixado com sucesso.")

# Execução principal do script
def main():
    driver = configurar_navegador(download_dir)
    wait = WebDriverWait(driver, 10)
    
    try:
        login(driver, wait)
        acessar_relatorio_e_preencher_datas(driver, wait)
        selecionar_opcoes_relatorio(driver, wait)
        baixar_csv(driver, wait, download_dir)
    finally:
        driver.quit()
        print("Operação Finalizada.")

if __name__ == "__main__":
    main()
