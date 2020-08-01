from SqlAlchemyHelper import *
from ModelAssociation import Model, SAMPLE_DATA, SAMPLE, FEATURE

class SampleData(Model):
    __tablename__ = SAMPLE_DATA

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    hash = Column(String(1024), unique=True)
    value = Column(Float(precision=12), nullable=False)
    iterationCount = Column(Integer(), nullable=False)
    sample, sampleId = getManyToOne(SAMPLE_DATA, SAMPLE, Model)
    feature, featureId = getManyToOne(SAMPLE_DATA, FEATURE, Model)

    def __init__(self,
        id = None,
        hash = None,
        value = None,
        iterationCount = None,
        sample = None,
        feature = None,
        sampleId = None,
        featureId = None
    ):
        self.id = id
        self.hash = hash
        self.value = value
        self.iterationCount = iterationCount
        self.sample = sample
        self.feature = feature
        self.sampleId = sampleId
        self.featureId = featureId

    def __repr__(self):
        return f'{self.__tablename__}(hash={self.hash}, value={self.value}, sample.key={self.sample.key if self.sample else None}, feature.key={self.feature.key if self.feature else None}, id={self.id})'
