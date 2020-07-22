class SkillDto :
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
