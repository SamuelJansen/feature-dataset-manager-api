from SqlAlchemyHelper import *
from ModelAssociation import Model, SKILL, SKILL_DATA, OWNER_DATA

class Skill(Model):
    __tablename__ = SKILL

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128),unique=True)
    label = Column(String(128))
    value = Column(Float(precision=12))
    skillDataList = getOneToMany(__tablename__, SKILL_DATA, Model)
    ownerDataList = getOneToMany(__tablename__, OWNER_DATA, Model)

    def __init__(self,
        id = None,
        key = None,
        label = None,
        value = None,
        skillDataList = None,
        ownerDataList = None
    ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        self.skillDataList = skillDataList if skillDataList else []
        self.ownerDataList = ownerDataList if ownerDataList else []

    def __repr__(self):
        return f'{SKILL}(id={self.id}, key={self.key}, label={self.label}, value={self.value})'
