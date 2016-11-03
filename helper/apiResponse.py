import json
from django.http import HttpResponse


# api response for user center
class ApiResponse():
    def __init__(self, codec, message = None, data = None):
        self.codec      = codec
        self.message    = message
        self.data       = data

    def json_message(self):
        if self.data:
            returnData = {'code' : self.codec, 'msg' : self.message, 'data' : self.data}
        else:
            returnData = {'code' : self.codec, 'msg' : self.message}

        return json.dumps(returnData)

    def json_response(self):
        data        = self.json_message()
        response    = HttpResponse(data, content_type = "application/json")
        return response

    def json_return(self):
        data        = self.json_message()
        return data


