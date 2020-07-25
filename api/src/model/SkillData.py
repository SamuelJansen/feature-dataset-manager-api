from SqlAlchemyHelper import *
from ModelAssociation import Model, SKILL_DATA, SKILL, OWNER

class SkillData(Model):
    __tablename__ = SKILL_DATA

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    hash = Column(String(1024), unique=True)
    value = Column(Float(precision=12))
    skill, skillId = getManyToOne(SKILL_DATA, SKILL, Model)
    owner, ownerId = getManyToOne(SKILL_DATA, OWNER, Model)

    def __init__(self,
        id = None,
        hash = None,
        value = None,
        skill = None,
        owner = None,
        skillId = None,
        ownerId = None
    ):
        self.id = id
        self.hash = hash
        self.value = value
        self.skill = skill
        self.owner = owner
        self.skillId = skillId
        self.ownerId = ownerId

    def __repr__(self):
        return f'{SKILL_DATA}(hash={self.hash}, value={self.value}, skill.label={self.skill.label}, owner.label={self.owner.label}, id={self.id})'
