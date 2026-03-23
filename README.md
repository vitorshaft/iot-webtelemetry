# IoT WebTelemetry - Monitoramento Fotovoltaico ☀️

Este projeto consiste em um sistema de telemetria de ponta a ponta para o monitoramento de módulos fotovoltaicos de Perovskita. O sistema utiliza um **ESP32** para coleta de dados em campo e um backend em **FastAPI (Python)** hospedado no **Render** para processamento e visualização.

## 🚀 Arquitetura do Sistema

O fluxo de dados segue a seguinte hierarquia:
1. **Hardware:** Sensor INA3221 conectado a um ESP32 realiza a leitura de Tensão (V), Corrente (mA) e Potência (mW).
2. **Firmware:** O ESP32 envia os dados via protocolo HTTP POST (JSON) para a API Cloud.
3. **Backend:** Servidor FastAPI recebe, valida (Pydantic) e armazena as leituras.
4. **Frontend:** Dashboard web simples para visualização de gráficos em tempo real.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
* **Hardware:** ESP32 (Framework Arduino/PlatformIO)
* **Sensores:** INA3221 (I2C)
* **Hospedagem:** [Render](https://render.com/)

## 📂 Estrutura do Repositório

```text
├── main.py              # Código principal da API FastAPI
├── requirements.txt     # Dependências do Python
├── firmware/            # (Opcional) Código fonte do ESP32 (PlatformIO)
└── README.md            # Documentação do projeto
```

## ⚙️ Instalação e Execução Local

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/iot-webtelemetry.git
    cd iot-webtelemetry
    ```

2.  **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Execute o servidor localmente:**
    ```bash
    uvicorn main:app --reload
    ```
    Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`

## 📡 Endpoints da API

* `GET /`: Status do sistema.
* `POST /telemetria`: Recebe dados do ESP32.
* `GET /dados`: Retorna o histórico de leituras para o Dashboard.

## 📝 Licença

Projeto desenvolvido para fins de monitoramento de energia renovável. Uso restrito conforme termos da consultoria.