# Teste Backend: Dashboard de Automação de Login com Python e Selenium

Este projeto implementa um dashboard web para executar e monitorar testes de login simultâneos em uma aplicação de exemplo. Construído com Python, Flask e Selenium, a ferramenta demonstra práticas profissionais de automação de testes, incluindo execução paralela, design patterns e relatórios visuais.

## Funcionalidades Principais

-   **Dashboard Interativo**: Interface web com design moderno (dark mode) para configurar e disparar os testes.
-   **Execução Paralela Eficiente**: Utiliza `ThreadPoolExecutor` para uma otimização massiva do tempo de execução em testes de larga escala.
-   **Métricas de Performance**: Apresenta um dashboard com métricas chave: tempo total, sucessos e falhas.
-   **Design Pattern Page Object Model (POM)**: O código de automação é estruturado com o padrão POM, garantindo alta manutenibilidade e escalabilidade.
-   **Relatórios Visuais com Captura de Tela**: Em caso de erro em qualquer teste, uma screenshot da tela do navegador é salva automaticamente em uma pasta dedicada (`errors-screenshoots`) para facilitar a depuração.
-   **Pronto para Deploy**: Estruturado para ser facilmente implantado em ambientes de produção com Gunicorn.

## Estrutura do Projeto

```
/login_simultaneo-record/
|-- static/
|   |-- style.css
|-- pages/
|   |-- __init__.py
|   |-- login_page.py
|-- templates/
|   |-- index.html
|-- errors-screenshoots/  
|-- app.py
|-- .env                   
|-- requirements.txt
|-- .gitignore            
```

## Pré-requisitos

-   Python 3.8 ou superior
-   Google Chrome instalado na máquina.

## Como Executar Localmente

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/mansque404/login-simultaneo-record.git](https://github.com/mansque404/login-simultaneo-record.git)
    cd nome-do-repositorio
    ```

2.  **Crie um Ambiente Virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    ```

3.  **Instale as Dependências**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Credenciais**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione o seguinte conteúdo a ele:
        ```.env
        LOGIN_USER="tomsmith"
        LOGIN_PASS="SuperSecretPassword!"
        ```

5.  **Execute a Aplicação**
    ```bash
    python app.py
    ```

6.  **Acesse o Dashboard**
    * Abra seu navegador e acesse: `http://127.0.0.1:5000`

## Deploy e Monitoramento

### **Deploy em Produção**

Para um ambiente de produção, utilize um servidor WSGI como o Gunicorn:

```bash
# O comando inicia 4 workers para lidar com requisições concorrentes
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
```
Este comando torna a aplicação acessível na porta 8000. Recomenda-se o uso de um proxy reverso como Nginx para gerenciar o tráfego, SSL, etc.

### **Monitoramento**

1.  **Logs de Aplicação**: Gunicorn e Flask geram logs de acesso e erro diretamente no console, que podem ser redirecionados para sistemas de gerenciamento de logs (ELK Stack, Splunk).

2.  **Artefatos de Teste**: A pasta `errors-screenshoots` serve como um sistema de monitoramento visual para falhas, permitindo uma análise rápida da causa raiz de problemas na interface.

3.  **Ferramentas de APM (Application Performance Monitoring)**: Para um monitoramento avançado, a aplicação pode ser integrada com serviços como Datadog, New Relic ou Sentry.