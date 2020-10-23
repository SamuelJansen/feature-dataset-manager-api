from python_framework import Repository
from python_framework import SqlAlchemyProxy as sap ###- exists 
import FeatureData, Feature, Sample

@Repository(model = FeatureData.FeatureData)
class FeatureDataRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsByKey(self, key) :
        return self.repository.existsByKeyAndCommit(key, self.model)

    def findByKey(self, key) :
        if self.existsByKey(key) :
            return self.repository.findByKeyAndCommit(key, self.model)
        return []

    def notExistsByKey(self, key) :
        return not self.existsByKey(key)

    def save(self,model) :
        return self.repository.saveAndCommit(model)

    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        objectExists = self.repository.session.query(
            self.repository.session.query(self.model).filter(
                sap.and_(
                    self.model.feature.has(Feature.Feature.key == featureKey),
                    self.model.sample.has(Sample.Sample.key == sampleKey)
                )
            ).exists()
        ).scalar()
        self.repository.session.commit()
        return objectExists

    def findByFeatureKeyAndSampleKey(self, featureKey, sampleKey) :
        featureData = self.repository.session.query(self.model).filter(
            sap.and_(
                self.model.feature.has(Feature.Feature.key == featureKey),
                self.model.sample.has(Sample.Sample.key == sampleKey)
            )
        ).first()
        self.repository.session.commit()
        return featureData

    def findAllByFeatureKey(self, featureKey) :
        featureDataList = self.repository.session.query(self.model).filter(self.model.feature.has(Feature.Feature.key == featureKey)).all()
        self.repository.session.commit()
        return featureDataList

    def findAllBySampleKey(self, sampleKey) :
        featureDataList = self.repository.session.query(self.model).filter(self.model.sample.has(Sample.Sample.key == sampleKey)).all()
        self.repository.session.commit()
        return featureDataList
