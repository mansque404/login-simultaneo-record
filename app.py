import os
import time
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from pages.login_page import LoginPage

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)


def perform_login(login_url: str, username: str, password: str) -> dict:
    """
    Executa uma única tentativa de login usando o Page Object Model
    e captura screenshots em uma pasta dedicada em caso de falha.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        login_page = LoginPage(driver)
        login_page.load(login_url)
        login_page.login(username, password)

        flash_message = login_page.get_flash_message()

        if "secure" in driver.current_url:
            return {"status": "Sucesso", "token": flash_message.split('×')[0].strip()}
        else:
            return {"status": "Falha", "message": flash_message.split('×')[0].strip()}

    except TimeoutException as e:
        logging.error(f"TimeoutException: {e}", exc_info=True)
        screenshot_dir = "errors-screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"erro_timeout_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, filename)
        
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot de erro salva em: {screenshot_path}")
        return {"status": "Falha", "message": "Timeout: A página ou um elemento demorou para carregar."}
    
    except Exception as e:
        logging.error(f"Erro inesperado no Selenium: {e}", exc_info=True)
        screenshot_dir = "errors-screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"erro_inesperado_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, filename)

        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot de erro salva em: {screenshot_path}")
        return {"status": "Falha", "message": f"Ocorreu um erro inesperado na automação."}
    
    finally:
        driver.quit()


@app.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')


@app.route('/execute_logins', methods=['POST'])
def execute_logins():
    """Endpoint que orquestra a execução dos logins simultâneos."""
    data = request.get_json()
    num_logins = data.get('num_logins', 1)
    
    logging.info(f"Recebida requisição para executar {num_logins} logins simultâneos.")

    LOGIN_URL = os.getenv("LOGIN_URL")
    USERNAME = os.getenv("LOGIN_USER")
    PASSWORD = os.getenv("LOGIN_PASS")

    if not USERNAME or not PASSWORD:
        logging.error("Credenciais não encontradas nas variáveis de ambiente (.env).")
        return jsonify({"error": "Credenciais de login não configuradas no servidor."}), 500

    start_time = time.time()
    
    results = []
    with ThreadPoolExecutor(max_workers=num_logins) as executor:
        future_logins = [executor.submit(perform_login, LOGIN_URL, USERNAME, PASSWORD) for _ in range(num_logins)]
        
        for future in as_completed(future_logins):
            try:
                results.append(future.result())
            except Exception as exc:
                logging.error(f"Erro gerado por uma thread: {exc}", exc_info=True)
                results.append({"status": "Falha", "message": f"Erro crítico na thread: {exc}"})

    total_time = time.time() - start_time
    logging.info(f"Execução de {num_logins} logins concluída em {total_time:.4f} segundos.")

    return jsonify({
        "total_time": total_time,
        "results": sorted(results, key=lambda x: x['status'], reverse=True)
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')