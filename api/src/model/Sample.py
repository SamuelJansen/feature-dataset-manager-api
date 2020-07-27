from SqlAlchemyHelper import *
from ModelAssociation import Model, SAMPLE, SAMPLE_DATA, FEATURE_DATA

class Sample(Model):
    __tablename__ = SAMPLE

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128),unique=True)
    label = Column(String(128))
    value = Column(Float(precision=12))
    sampleDataList = getOneToMany(__tablename__, SAMPLE_DATA, Model)
    featureDataList = getOneToMany(__tablename__, FEATURE_DATA, Model)

    def __init__(self,
        id = None,
        key = None,
        label = None,
        value = None,
        sampleDataList = None,
        featureDataList = None
    ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        self.sampleDataList = sampleDataList if sampleDataList else []
        self.featureDataList = featureDataList if featureDataList else []

    def __repr__(self):
        return f'{SAMPLE}(id={self.id}, key={self.key}, label={self.label}, value={self.value})'
