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

from fastapi import FastAPI, Header
from ToposoidCommon.model import StatusInfo, TransversalState, SingleSentence, DetectedLanguage
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from typing import Optional

import traceback

from middleware import ErrorHandlingMiddleware
import ToposoidCommon as tc

LOG = tc.LogUtils(__name__)

app = FastAPI(
    title="toposoid-language-detector-web",
    version="0.6-SNAPSHOT"
)
app.add_middleware(ErrorHandlingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/detectLanguage",
          summary='Automatically detect the language of a text')
def detectLanguage(singleSentence:SingleSentence, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:
        LOG.info(f"Input:{singleSentence.sentence}", transversalState)           
        detectedLanguage:DetectedLanguage = tc.detectLangage(singleSentence.sentence) 
        response = JSONResponse(content=jsonable_encoder(detectedLanguage))
        LOG.info(f"Lang Detection completed.[lang:{detectedLanguage.lang}]", transversalState)
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(DetectedLanguage(lang="")))

      

