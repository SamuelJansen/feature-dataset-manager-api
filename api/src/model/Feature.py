from SqlAlchemyHelper import *
from ModelAssociation import Model, FEATURE, FEATURE_DATA, SAMPLE_DATA

class Feature(Model):
    __tablename__ = FEATURE

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128), unique=True)
    label = Column(String(128))
    value = Column(Float(precision=12))
    iterationCount = Column(Integer())
    featureDataList = getOneToMany(__tablename__, FEATURE_DATA, Model)
    sampleDataList = getOneToMany(__tablename__, SAMPLE_DATA, Model)

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

    def __repr__(self):
        return f'{FEATURE}(id={self.id}, key={self.key}, label={self.label}, value={self.value})'
