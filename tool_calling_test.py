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
        
    def run_model(self) -> List[Data]:
        return self._send_request_get_list_meeting(self.userId)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="getListMeeting",
            description="A tool that get list of meetings invited or created",
            func=self._send_request_get_list_meeting_direct,
            args_schema=self.GetListMeetingToolSchema,
        )

1 validation error for GetListMeetingToolSchema
userId
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.10/v/missing  
