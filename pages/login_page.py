from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Esta classe encapsula todos os elementos e ações da página de login,
    seguindo o padrão Page Object Model (POM).
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        self._username_input = (By.ID, "username")
        self._password_input = (By.ID, "password")
        self._submit_button = (By.CSS_SELECTOR, "button[type='submit']")
        self._flash_message = (By.ID, "flash")

    def load(self, url: str):
        """Carrega a URL da página de login no navegador."""
        self.driver.get(url)

    def login(self, username: str, password: str):
        """Executa a ação de preencher o formulário e submeter."""
        self.wait.until(EC.visibility_of_element_located(self._username_input)).send_keys(username)
        self.driver.find_element(*self._password_input).send_keys(password)
        self.driver.find_element(*self._submit_button).click()

    def get_flash_message(self) -> str:
        """Aguarda e retorna o texto da mensagem de feedback (sucesso ou erro)."""
        return self.wait.until(EC.visibility_of_element_located(self._flash_message)).text