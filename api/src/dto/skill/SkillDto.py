class SkillDto :
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
