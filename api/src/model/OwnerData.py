from SqlAlchemyHelper import *
from ModelAssociation import Model, OWNER_DATA, OWNER, SKILL

class OwnerData(Model):
    __tablename__ = OWNER_DATA

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    hash = Column(String(1024), unique=True)
    value = Column(Float(precision=12))
    owner, ownerId = getManyToOne(OWNER_DATA, OWNER, Model)
    skill, skillId = getManyToOne(OWNER_DATA, SKILL, Model)

    def __init__(self,
        id = None,
        hash = None,
        value = None,
        owner = None,
        skill = None,
        ownerId = None,
        skillId = None
    ):
        self.id = id
        self.hash = hash
        self.value = value
        self.owner = owner
        self.skill = skill
        self.ownerId = ownerId
        self.skillId = skillId

    def __repr__(self):
        return f'{OWNER_DATA}(hash={self.hash}, value={self.value}, owner.label={self.owner.label}, skill.label={self.skill.label}, id={self.id})'
