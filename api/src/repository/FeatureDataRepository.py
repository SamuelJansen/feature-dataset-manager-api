from FlaskHelper import Repository
import FeatureData

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

    def findAllBySampleKey(self, sampleKey) :
        featureDataList = self.repository.session.query(self.model).filter(self.model.sample.key == sampleKey).all()
        self.repository.session.commit()
        return featureDataList
