from python_framework import SqlAlchemyProxy as sap
from ModelAssociation import Model, SAMPLE, SAMPLE_DATA, FEATURE_DATA

class Sample(Model):
    __tablename__ = SAMPLE

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    key = sap.Column(sap.String(128), unique=True, nullable=False)
    label = sap.Column(sap.String(128))
    value = sap.Column(sap.Float(precision=12), nullable=False)
    iterationCount = sap.Column(sap.Integer(), nullable=False)
    sampleDataList = sap.getOneToMany(__tablename__, SAMPLE_DATA, Model)
    featureDataList = sap.getOneToMany(__tablename__, FEATURE_DATA, Model)

    def __init__(self,
        id = None,
        key = None,
        label = None,
        value = None,
        iterationCount = None,
        sampleDataList = None,
        featureDataList = None
    ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        self.iterationCount = iterationCount
        self.sampleDataList = sampleDataList if sampleDataList else []
        self.featureDataList = featureDataList if featureDataList else []

    def __repr__(self):
        return f'{self.__tablename__}(id={self.id}, key={self.key}, label={self.label}, value={self.value})'
