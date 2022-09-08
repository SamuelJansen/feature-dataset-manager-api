class FeatureRequestDto :
    def __init__(self,
        label = None
    ):
        self.label = label

class FeatureResponseDto :
    def __init__(self,
        key = None,
        label = None,
        value = None,
        iterationCount = None
    ):
        self.key = key
        self.label = label
        self.value = value
        self.iterationCount = iterationCount
