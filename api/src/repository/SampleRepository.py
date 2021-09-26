from python_framework import Repository

from Sample import Sample

@Repository(model = Sample)
class SampleRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsByKey(self,key) :
        return self.repository.existsByKeyAndCommit(key, self.model)

    def findByKey(self,key) :
        if self.existsByKey(key) :
            return self.repository.findByKeyAndCommit(key, self.model)

    def notExistsByKey(self,key) :
        return not self.existsByKey(key)

    def save(self,model) :
        return self.repository.saveAndCommit(model)

    def deleteByKey(self,key):
        self.repository.deleteByKeyAndCommit(key, self.model)

    def findAllByFeatureKeyIn(self, featureKeyList):
        sampleList = []
        for sample in self.repository.session.query(self.model) :
            keepIt = False
            for key in featureKeyList :
                for featureData in sample.featureDataList :
                    if featureData.feature.key == key :
                        keepIt = True
                        sampleList.append(sample)
                        break
                if keepIt :
                    break
        return sampleList

    def findAllByAllFeatureKeyIn(self, featureKeyList):
        sampleList = []
        for sample in self.repository.session.query(self.model) :
            keepIt = True
            for key in featureKeyList :
                keepIt = False
                for featureData in sample.featureDataList :
                    if featureData.feature.key == key :
                        keepIt = True
                        break
                if not keepIt :
                    break
            if keepIt :
                sampleList.append(sample)
        return sampleList
