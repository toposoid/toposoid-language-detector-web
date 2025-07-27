'''
  Copyright (C) 2025  Linked Ideal LLC.[https://linked-ideal.com/]
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, version 3.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.
 
  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

        
        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json=jsonable_encoder(SingleSentence(sentence="NO_REFERENCE_5d9afee2-4c10-11f0-9f26-acde48001122_1") ))
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert detectedLanguage.lang == "@@_#1"
        


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

    
