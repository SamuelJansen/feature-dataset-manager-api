class OwnerDto :
    def __init__(self,
            id = None,
            key = None,
            label = None,
            value = None,
            skillList = None
        ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        if skillList :
            self.skillList = skillList
        else :
            self.skillList = []
