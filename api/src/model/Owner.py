from SqlAlchemyHelper import *
from ModelAssociation import Model, OWNER, OWNER_DATA, SKILL_DATA

class Owner(Model):
    __tablename__ = OWNER

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128),unique=True)
    label = Column(String(128))
    value = Column(Float(precision=12))
    ownerDataList = getOneToMany(__tablename__, OWNER_DATA, Model)
    skillDataList = getOneToMany(__tablename__, SKILL_DATA, Model)

    def __init__(self,
        id = None,
        key = None,
        label = None,
        value = None,
        ownerDataList = None,
        skillDataList = None
    ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        self.ownerDataList = ownerDataList if ownerDataList else []
        self.skillDataList = skillDataList if skillDataList else []

    def __repr__(self):
        return f'{OWNER}(id={self.id}, key={self.key}, label={self.label}, value={self.value})'
