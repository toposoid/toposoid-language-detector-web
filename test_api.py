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
from ToposoidCommon import StatusInfo
from fastapi.testclient import TestClient
from api import app
import pytest
from ToposoidCommon.model import TransversalState, DetectedLanguage
from time import sleep
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

class TestToposoidLanguageDetectorWeb(object):

    client = TestClient(app)
    transversalState = str(jsonable_encoder(TransversalState(userId="test-user", username="guest", roleId=0, csrfToken = "")))
        
    def test_detectLanguage(self):   
        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json={"sentence": "これは日本語ですか？"})
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert detectedLanguage.lang == "ja_JP"

    def test_detectLanguage2(self):      
        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json={"sentence": "Is This English?"})
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert detectedLanguage.lang == "en_US"

    def test_detectLanguage3(self):         
        response = self.client.post("/detectLanguage",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": self.transversalState},
                            json={"sentence": "è questo italiano?"})
        assert response.status_code == 200
        detectedLanguage = DetectedLanguage.parse_obj(response.json())
        assert  detectedLanguage.lang == ""        
