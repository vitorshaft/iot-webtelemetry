from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI(title="Soliverde IoT Gateway")

# Modelo de dados que o ESP32 vai enviar
class LeituraTelemetria(BaseModel):
    id_modulo: str
    tensao: float
    corrente: float
    potencia: float

# Banco de dados temporário (em memória) para teste
historico_leituras = []

@app.get("/")
def home():
    return {"status": "Online", "projeto": "Monitoramento Perovskita", "timestamp": datetime.now()}

@app.post("/telemetria")
async def receber_dados(leitura: LeituraTelemetria):
    # Aqui adicionamos um timestamp do servidor
    dados_com_hora = leitura.dict()
    dados_com_hora["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    historico_leituras.append(dados_com_hora)
    
    # Mantém apenas as últimas 50 leituras em memória para não estourar o tier gratuito
    if len(historico_leituras) > 50:
        historico_leituras.pop(0)
        
    print(f"Recebido de {leitura.id_modulo}: {leitura.tensao}V")
    return {"message": "Dados recebidos com sucesso", "count": len(historico_leituras)}

@app.get("/dados")
def listar_dados():
    return historico_leituras