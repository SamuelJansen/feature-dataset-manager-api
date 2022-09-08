import globals
from python_helper import Constant as c
from python_helper import ObjectHelper, StringHelper, ReflectionHelper
from python_framework import Repository
from python_framework import SqlAlchemyProxy as sap ###- exists

from Sample import Sample
from Feature import Feature
from FeatureData import FeatureData

@Repository(model = FeatureData)
class FeatureDataRepository:

    def findAll(self):
        return self.repository.findAllAndCommit(self.model)

    def existsByKey(self, key):
        return self.repository.existsByKeyAndCommit(key, self.model)

    def findByKey(self, key):
        if self.existsByKey(key):
            return self.repository.findByKeyAndCommit(key, self.model)
        return []

    def notExistsByKey(self, key):
        return not self.existsByKey(key)

    def save(self,model):
        return self.repository.saveAndCommit(model)

    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        objectExists = self.repository.session.query(
            self.repository.session.query(self.model).filter(
                sap.and_(
                    self.model.feature.has(Feature.key == featureKey),
                    self.model.sample.has(Sample.key == sampleKey)
                )
            ).exists()
        ).scalar()
        self.repository.session.commit()
        return objectExists

    def findByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        featureData = self.repository.session.query(self.model).filter(
            sap.and_(
                self.model.feature.has(Feature.key == featureKey),
                self.model.sample.has(Sample.key == sampleKey)
            )
        ).first()
        self.repository.session.commit()
        return featureData

    def findAllByFeatureKey(self, featureKey):
        featureDataList = self.repository.session.query(self.model).filter(self.model.feature.has(Feature.key == featureKey)).all()
        self.repository.session.commit()
        return featureDataList

    def findAllBySampleKey(self, sampleKey):
        featureDataList = self.repository.session.query(self.model).filter(self.model.sample.has(Sample.key == sampleKey)).all()
        self.repository.session.commit()
        return featureDataList

    def existsByFeatureKey(self, featureKey):
        exists = self.repository.session.query(self.model).filter(self.model.feature.has(Feature.key == featureKey)).scalar()
        self.repository.session.commit()
        return exists

    def existsBySampleKey(self, sampleKey):
        exists = self.repository.session.query(self.model).filter(self.model.sample.has(Sample.key == sampleKey)).scalar()
        self.repository.session.commit()
        return exists

    def findAllByQuery(self, query):
        finalQuery = self.repository.session.query(self.model)
        for k, v in {k:v for k,v in query.items() if ObjectHelper.isNotNone(v)}.items():
            titleList = StringHelper.toTitle(k).split()
            if 1 == len(titleList):
                finalQuery = finalQuery.filter(ReflectionHelper.getAttributeOrMethod(self.model, k.lower()) == v)
            elif 1 < len(titleList):
                relationship = ReflectionHelper.getAttributeOrMethod(self.model, titleList[0].lower())
                resource = globals.importResource(titleList[0], required=True)
                resourceAttributeName = StringHelper.toCamelCase(
                    StringHelper.join(titleList[1:], character=c.BLANK )
                )
                finalQuery = finalQuery.join(
                    resource,
                    relationship
                ).filter(
                    relationship.has(
                        ReflectionHelper.getAttributeOrMethod(
                            resource,
                            resourceAttributeName
                        ) == v
                    )
                )
            # if 'featureKey' == k:
            #     finalQuery = finalQuery.join(Feature, self.model.feature).filter(self.model.feature.has(Feature.key == v))
            # if 'sampleKey' == k:
            #     finalQuery = finalQuery.join(Sample, self.model.sample).filter(self.model.sample.has(Sample.key == v))
        # modelList = self.repository.session.query(self.model).filter(correctQuery).all()
        modelList = finalQuery.all()
        self.repository.session.commit()
        return modelList
