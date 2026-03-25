from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()


class TipoRecurso(enum.Enum):
    PERSONAJE = 'personaje'
    VEHICULO = 'vehiculo'
    LUGAR = 'lugar'
    CRIATURA = 'criatura'
    DROIDE = 'droide'
    ORGANIZACION = 'organizacion'
    ESPECIE = 'especie'


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favoritos: Mapped[List['Favorito']] = relationship(
        back_populates='user', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active,
            "total_favoritos": len(self.favoritos),
            "favoritos": [favorito.serialize() for favorito in self.favoritos]
        }


class Favorito(db.Model):
    __tablename__ = 'favorito'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    recurso_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[TipoRecurso] = mapped_column(
        Enum(TipoRecurso), nullable=False)

    user: Mapped['User'] = relationship(back_populates='favoritos')

    def serialize(self):
        mapeo = {
            TipoRecurso.PERSONAJE: Personaje,
            TipoRecurso.VEHICULO: Vehiculo,
            TipoRecurso.LUGAR: Lugar,
            TipoRecurso.CRIATURA: Criatura,
            TipoRecurso.DROIDE: Droide,
            TipoRecurso.ORGANIZACION: Organizacion,
            TipoRecurso.ESPECIE: Especie,
        }

        modelo_destino = mapeo.get(self.tipo)

        detalles = db.session.get(
            modelo_destino, self.recurso_id) if modelo_destino else None

        return {
            "id": self.id,
            # "recurso_id": self.recurso_id,
            "tipo": self.tipo.value,
            "name": detalles.name,
            "description": detalles.description,
            "image": detalles.image
        }


class BaseRecurso:
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image
        }


class Personaje(db.Model, BaseRecurso):
    __tablename__ = 'personaje'


class Vehiculo(db.Model, BaseRecurso):
    __tablename__ = 'vehiculo'


class Lugar(db.Model, BaseRecurso):
    __tablename__ = 'lugar'


class Criatura(db.Model, BaseRecurso):
    __tablename__ = 'criatura'


class Droide(db.Model, BaseRecurso):
    __tablename__ = 'droide'


class Organizacion(db.Model, BaseRecurso):
    __tablename__ = 'organizacion'


class Especie(db.Model, BaseRecurso):
    __tablename__ = 'especie'
