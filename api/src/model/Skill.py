from SqlAlchemyHelper import *
from ModelAssociation import Model, SKILL, OWNER, skillToOwnerAssociation

class Skill(Model):
    __tablename__ = SKILL

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128),unique=True)
    label = Column(String(128))
    value = Column(Float(precision=12))
    ownerList = relationship(OWNER, secondary=skillToOwnerAssociation, back_populates=attributeIt(f'{__tablename__}{LIST}'))

    def __init__(self,
            id = None,
            key = None,
            label = None,
            value = None,
            ownerList = None
        ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        if ownerList :
            self.ownerList = ownerList
        else :
            self.ownerList = []

    def __repr__(self):
        return f'{SKILL}(id={self.id}, key={self.key}, label={self.label}, value={self.value})'
