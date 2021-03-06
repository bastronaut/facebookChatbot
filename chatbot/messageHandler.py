from flask import Flask, request
app = Flask(__name__)
import json
import requests
from database.db import Db
from responseBuilder import ResponseBuilder
from messageEntity import MessageEntity


class MessageHandler:
    db = Db()
    rb = ResponseBuilder()

    def buildResponseForRequest(self, payload):

        messaging = payload["entry"][0]["messaging"]
        timestamp = payload["entry"][0]["time"]

        for event in messaging:
            if "message" in event and "text" in event["message"]:
                messagesender = event["sender"]["id"]
                messagetext = event["message"]["text"]
                print 'sender: ', messagesender, ' text: ', messagetext
                messageEntity = MessageEntity(messagesender, messagetext)
                self.db.storeIncomingMsg(messagesender, messagetext, timestamp)

                ### temporary multiple choice test
                if messagetext == 'multiplechoice!':
                    return {'messagesender' : messagesender,
                            'responsetext' : 'multiplechoice!',
                            'timestamp': timestamp}

                responses = self.rb.getResponsesForMessage(messageEntity)
                if responses:
                    return {'messagesender' : messagesender,
                            'responsetext' : responses[0]["responseText"],
                            'timestamp': timestamp}
                else:
                    return False


    def sendResponse(self, response, token):
        print 'building response for:\n', response
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
            "recipient": {"id": response["messagesender"]},
            "message": {"text": response["responsetext"]}
        }),
        headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print 'request codes not ok:', r.text
        else:
            print 'response done, inserting outgoing msg into db'
            self.db.storeOutgoingMsg(response["messagesender"], response["responsetext"], response["timestamp"])
        return 'ok'


    def testMultipleChoiceResponse(self, response, token):
        print 'building test response'
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": token},
        data=json.dumps({
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
        }),
        headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print 'request codes not ok:', r.text
        else:
            print 'response done, inserting outgoing msg into db'
            self.db.storeOutgoingMsg(response["messagesender"], response["responsetext"], response["timestamp"])
        return 'ok'
