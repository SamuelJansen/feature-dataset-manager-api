from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import Model, SAMPLE_DATA, SAMPLE, FEATURE

class SampleData(Model):
    __tablename__ = SAMPLE_DATA

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    hash = sap.Column(sap.String(1024), unique=True)
    value = sap.Column(sap.Float(precision=12), nullable=False)
    iterationCount = sap.Column(sap.Integer(), nullable=False)
    sample, sampleId = sap.getManyToOne(__tablename__, SAMPLE, Model)
    feature, featureId = sap.getManyToOne(__tablename__, FEATURE, Model)

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
