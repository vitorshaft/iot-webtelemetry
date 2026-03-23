import os
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configurações de Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do Banco de Dados
class LeituraDB(Base):
    __tablename__ = "telemetria"
    id = Column(Integer, primary_key=True, index=True)
    id_modulo = Column(String)
    tensao = Column(Float)
    corrente = Column(Float)
    potencia = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

# Cria a tabela se não existir
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Segurança (API Key)
API_KEY = os.getenv("X_API_KEY", "chave_padrao_apenas_para_local")
api_key_header = APIKeyHeader(name="X-API-KEY")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY: return api_key
    raise HTTPException(status_code=403, detail="Chave Inválida")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Dependência do Banco
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Schemas Pydantic
class TelemetriaSchema(BaseModel):
    id_modulo: str
    tensao: float
    corrente: float
    potencia: float

@app.post("/telemetria")
def salvar_dados(dados: TelemetriaSchema, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    nova_leitura = LeituraDB(**dados.dict())
    db.add(nova_leitura)
    db.commit()
    return {"status": "salvo no postgres"}

@app.get("/dados")
def listar_dados(db: Session = Depends(get_db)):
    # Retorna as últimas 100 leituras
    return db.query(LeituraDB).order_by(LeituraDB.timestamp.desc()).limit(100).all()