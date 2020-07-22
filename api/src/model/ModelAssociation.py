from SqlAlchemyHelper import *

Model = getNewModel()

SKILL = 'Skill'
OWNER = 'Owner'
skillToOwnerAssociation = getManyToMany(SKILL, OWNER, Model)
