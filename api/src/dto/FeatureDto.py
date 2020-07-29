class FeatureDto :
    def __init__(self,
        id = None,
        key = None,
        label = None,
        value = None,
        iterationCount = None,
        featureDataList = None,
        sampleDataList = None
    ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        self.iterationCount = iterationCount
        self.featureDataList = featureDataList if featureDataList else []
        self.sampleDataList = sampleDataList if sampleDataList else []

class FeatureRequestDto :
    def __init__(self,
        label = None
    ):
        self.label = label

class FeatureResponseDto :
    def __init__(self,
        key = None,
        label = None,
        iterationCount = None###- ,
        # featureDataList = None,
        # sampleDataList = None
    ):
        self.key = key
        self.label = label
        self.iterationCount = iterationCount
        # self.featureDataList = featureDataList if featureDataList else []
        # self.sampleDataList = sampleDataList if sampleDataList else []


class FeaturePostRequestDto :
    def __init__(self,
        key = None,
        label = None
    ):
        self.key = key
        self.label = label
