import ast
import operator
from typing import List
from pydantic import BaseModel, Field
from langflow.base.langchain_utilities.model import LCToolComponent
from langflow.inputs import MessageTextInput
from langflow.schema import Data
from langflow.field_typing import Tool
from langchain.tools import StructuredTool
import requests
import json
import hmac
import hashlib
import base64
import time


class GetListMeetingToolComponent(LCToolComponent):
    display_name = "GetListMeetingTool"
    description = "A tool that get list of meetings invited or created"
    #icon = "calculator"
    name = "GetListMeetingTool"

    inputs = [
        MessageTextInput(
            name="userId",
            display_name="userId",
            info="user email id"
        ),    
    ]

    class GetListMeetingToolSchema(BaseModel):
        userId: str = Field(..., description="user email id (e.g., 'kay.cho@samsung.com').")
        
    def run_model(self, userId: str) -> List[Data]:
        return self._send_request_get_list_meeting_direct(userId)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="getListMeeting",
            description="A tool that get list of meetings invited or created",
            func=self._send_request_get_list_meeting_direct,
            args_schema=self.GetListMeetingToolSchema,
        )

    def _send_request_get_list_meeting_direct(self, userId: str) -> List[Data]:
        current_time = time.time()
        timestamp = int(current_time * 1000)
        hmac_base64 = self.gen_hmac(timestamp)
        
        url = "https://stg.meeting.samsung.net/front/v1/conferences"                
        headers = {"Content-Type": "application/json; charset=utf-8", "Client-Code": "BrityAuto", "Hmac": hmac_base64, "Requester-Id": "kay.cho@stage.samsung.com", "Timestamp": str(timestamp)}
        params = {"statuses":"10"} 
        
        response = requests.get(url, headers=headers, params=params)
        
        # parameters_to_select = ['title', 'hostEmail', 'reservedDate', 'conferenceNo', 'participants'] 
        json_data = json.loads(response.text).get('data').get('dataList')
        
        filtered_data = []
        for item in json_data:
            participants = item["participants"]
            filtered_participants = [user["email"] for user in participants]
            chunk = {"conferenceNo": item["conferenceNo"], 
             "title": item["title"], 
             "reservedDate": item["reservedDate"], 
             "hostEmail": item["hostEmail"], 
             "participants": filtered_participants}
            filtered_data.append(chunk)        
        
        print("Status Code", response.status_code)

        return filtered_data

    def gen_hmac(self, timestamp):
        hmac_key = 'HySnCe9Ks3K6W2Or'

        # Data string constructed from the request
        data = f'{str(timestamp)}GET/front/v1/conferences10'
        self.log(data)

        # Generate HMAC-SHA256 and encode in Base64
        hmac_value = hmac.new(hmac_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
        hmac_base64 = base64.b64encode(hmac_value).decode('utf-8')
        return hmac_base64


# 1 validation error for GetListMeetingToolSchema
# userId
#   Field required [type=missing, input_value={}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.10/v/missing  
