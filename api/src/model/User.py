from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import Model, USER
import Role

class User(Model):
    __tablename__ = USER

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(128),unique=True, nullable=False)
    role = sap.Column(sap.String(128), nullable=False)
    username = sap.Column(sap.String(128),unique=True, nullable=False)
    password = sap.Column(sap.String(128), nullable=False)
    email = sap.Column(sap.String(128), nullable=False, default=Role.USER)

    def __init__(self,
        id = None,
        key = None,
        role = None,
        username = None,
        password = None,
        email = None
    ):
        self.id = id
        self.key = key
        self.role = role
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, role={self.role}, username={self.username}, email={self.email})'
