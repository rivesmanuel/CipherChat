from app import db
import datetime
from sqlalchemy import JSON, DateTime, Integer, String, Text, Float
from sqlalchemy import Boolean, Column , ForeignKey


class Conversacion(db.Model):
    __tablename__ = 'conversaciones'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), default="default_user")
    mensajes = Column(JSON)
    creado = Column(DateTime, default=datetime.datetime.utcnow)
    actualizado = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
