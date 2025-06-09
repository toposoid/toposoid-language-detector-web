'''
  Copyright 2021 Linked Ideal LLC.[https://linked-ideal.com/]
 
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
      http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 '''
from ToposoidCommon import SingleSentence
from ToposoidCommon.model import TransversalState, Knowledge, PropositionRelation, KnowledgeSentenceSet, DetectedLanguage
from fastapi.testclient import TestClient
from api import app
import pytest
from time import sleep
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

class TestToposoidLanguageDetectorWeb(object):

    client = TestClient(app)
    transversalState = str(jsonable_encoder(TransversalState(userId="test-user", username="guest", roleId=0, csrfToken = "")))

    def test_detectLanguage(self):         
        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json=jsonable_encoder(SingleSentence(sentence="これは日本語です。") ))
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert detectedLanguage.lang == "ja_JP"

        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json=jsonable_encoder(SingleSentence(sentence="This is English.") ))
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert detectedLanguage.lang == "en_US"

        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json=jsonable_encoder(SingleSentence(sentence="è questo italiano?") ))
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert detectedLanguage.lang == ""


    def test_detectLanguages(self): 
        knowledge1 = Knowledge(sentence = "これはテストの前提1です。", lang = "", extentInfoJson = "{}")
        knowledge2 = Knowledge(sentence = "This is Premise2.", lang = "", extentInfoJson = "{}")

        knowledge3 = Knowledge(sentence = "これはテストの主張1です。", lang = "", extentInfoJson = "{}")
        knowledge4 = Knowledge(sentence = "This is Claim2", lang = "", extentInfoJson = "{}")
        knowledge5 = Knowledge(sentence = "è questo italiano?", lang = "", extentInfoJson = "{}")

        knowledgeSentenceSet = KnowledgeSentenceSet(
            premiseList = [knowledge1, knowledge2],
            premiseLogicRelation = [PropositionRelation(operator = "AND", sourceIndex = 0, destinationIndex = 1)],
            claimList = [knowledge3, knowledge4, knowledge5],
            claimLogicRelation = [PropositionRelation(operator = "OR", sourceIndex = 0, destinationIndex = 1), PropositionRelation(operator = "OR", sourceIndex = 0, destinationIndex = 2)]
        )

        response = self.client.post("/detectLanguages",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json=jsonable_encoder(knowledgeSentenceSet))
        assert response.status_code == 200
        resKnowledgeSentenceSet = KnowledgeSentenceSet.parse_obj(response.json())
        assert resKnowledgeSentenceSet.premiseList[0].lang == "ja_JP"
        assert resKnowledgeSentenceSet.premiseList[1].lang == "en_US"
        
        assert resKnowledgeSentenceSet.claimList[0].lang == "ja_JP"
        assert resKnowledgeSentenceSet.claimList[1].lang == "en_US"
        assert resKnowledgeSentenceSet.claimList[2].lang == ""

    
