from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import Model, FEATURE_DATA, FEATURE, SAMPLE

class FeatureData(Model):
    __tablename__ = FEATURE_DATA

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    hash = sap.Column(sap.String(1024), unique=True)
    value = sap.Column(sap.Float(precision=12), nullable=False)
    iterationCount = sap.Column(sap.Integer(), nullable=False)
    feature, featureId = sap.getManyToOne(FEATURE_DATA, FEATURE, Model)
    sample, sampleId = sap.getManyToOne(FEATURE_DATA, SAMPLE, Model)

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
        return f'{self.__tablename__}(hash={self.hash}, value={self.value}, feature.key={self.feature.key if self.feature else None}, sample.key={self.sample.key if self.sample else None}, id={self.id})'
