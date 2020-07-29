from SqlAlchemyHelper import *
from ModelAssociation import Model, FEATURE_DATA, FEATURE, SAMPLE

class FeatureData(Model):
    __tablename__ = FEATURE_DATA

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    hash = Column(String(1024), unique=True)
    value = Column(Float(precision=12))
    iterationCount = Column(Integer())
    feature, featureId = getManyToOne(FEATURE_DATA, FEATURE, Model)
    sample, sampleId = getManyToOne(FEATURE_DATA, SAMPLE, Model)

    def __init__(self,
        id = None,
        hash = None,
        value = None,
        iterationCount = None,
        feature = None,
        sample = None,
        featureId = None,
        sampleId = None
    ):
        self.id = id
        self.hash = hash
        self.value = value
        self.iterationCount = iterationCount
        self.feature = feature
        self.sample = sample
        self.featureId = featureId
        self.sampleId = sampleId

    def __repr__(self):
        return f'{FEATURE_DATA}(hash={self.hash}, value={self.value}, feature.key={self.feature.key if self.feature else None}, sample.key={self.sample.key if self.sample else None}, id={self.id})'
