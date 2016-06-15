
class ButtonMessage:

    def __init__(self):

    jsonresponse =json.dumps({
        "recipient": {"id": response["messagesender"]},
        "message":{
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"button",
                "text":"What do you want to do next?",
                "buttons":[
                  {
                    "type":"postback",
                    "title" : "First postbak",
                    "payload":"ANOTHER_PAYLOAD"
                  },
                  {
                    "type":"postback",
                    "title":"Start Chatting",
                    "payload":"USER_DEFINED_PAYLOAD"
                  }
                ]
              }
            }
          }
    })
