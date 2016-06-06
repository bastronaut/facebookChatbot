#!/usr/bin/python
'''
        1
     /      \
    2         4
    |       /   \
    3       5   6
                |
                7

'''


class Sampledata:

    def getConversations(self):
        return self.convs

    def getTestconversationState(self):
        return self.testconversationstate

    def getMessages(self):
        return self.messages

    def getgraphmessages(self):
        return self.graphmessages

    def getTestJSONs(self):
        return self.testJSONS

    convs = [
        {"conv_id": 1, "conv_name": "example chat"},
        {"conv_id": 2, "conv_name": "second chat"},
        # {"conv_id": 3, "conv_name": "third chat"}
    ]

    messages = [
     {"m_nr": 1, "qtext": "Hi", "rtext": "Hi! :) How are you?", "is_alternative": False, "conv_id": 1, "key": 123},
     {"m_nr": 2, "qtext": "Good!", "rtext": "That's great to hear!", "is_alternative": True, "conv_id": 1, "key": 124},
     {"m_nr": 3, "qtext": "Bad!", "rtext": "I'm sorry to hear that", "is_alternative": True, "conv_id": 1, "key": 125},
     {"m_nr": 4, "qtext": "OK", "rtext": "nice", "is_alternative": True, "conv_id": 1, "key": 126},
     {"m_nr": 5, "qtext": "How about you?", "rtext": "I'm doing just fine!", "is_alternative": False, "conv_id": 1, "key": 127},
     {"m_nr": 1, "qtext": "Food", "rtext": "Can I order you anything?", "is_alternative": False, "conv_id": 2, "key": 128},
     {"m_nr": 2, "qtext": "Pizza", "rtext": "Ordering you a pizza as we speak!", "is_alternative": True, "conv_id": 2, "key": 129},
     {"m_nr": 3, "qtext": "Burrito", "rtext": "Ordering you a burrito as we speak!", "is_alternative": True, "conv_id": 2, "key": 130},
    ]

    graphmessages = [
        {"m_nr": 1, "qtext": "Hi", "rtext": "Hi! :) How are you?",  "conv_id": 1, "key": 123, "parent": 0, "children": set([124, 126])},
        {"m_nr": 2, "qtext": "Good!", "rtext": "That's great to hear!", "conv_id": 1, "key": 124, "parent": 123, "children": set([125])},
        {"m_nr": 3, "qtext": "Thanks!", "rtext": "No Problem!", "conv_id": 1, "key": 125, "parent": 124, "children": set([])},
        {"m_nr": 4, "qtext": "Not great...", "rtext": "How come?", "conv_id": 1, "key": 126, "parent": 123, "children": set([127, 128])},
        {"m_nr": 5, "qtext": "Feeling sick", "rtext": "Aww. Get well soon!", "conv_id": 1, "key": 127, "parent": 126, "children": set([])},
        {"m_nr": 6, "qtext": "Feeling tired", "rtext": "Aww. Get some sleep!", "conv_id": 1, "key": 128, "parent": 126, "children": set([129])},
        {"m_nr": 7, "qtext": "I will!", "rtext": "Good night!", "conv_id": 1, "key": 129, "parent": 0, "children": set([])},
    ]
    testconversationstate = {
        123: [
            {'conv_id': 1, 'latestinteraction': 10, 'mostrecentquestion': 2.2},
            {'conv_id': 2, 'latestinteraction': 30, 'mostrecentquestion': 2},
        ],
        456: [
            {'conv_id': 2, 'latestinteraction': 44, 'mostrecentquestion': 1},
            {'conv_id': 3, 'latestinteraction': 30, 'mostrecentquestion': 5},
            {'conv_id': 1, 'latestinteraction': 2, 'mostrecentquestion': 3},
        ],
        789: [
            {'conv_id': 5, 'latestinteraction': 21, 'mostrecentquestion': 1},
            {'conv_id': 4, 'latestinteraction': 30, 'mostrecentquestion': 1},
            {'conv_id': 1, 'latestinteraction': 2, 'mostrecentquestion': 3},
        ]
    }

    testJSONS = ['''{
      "object":"page",
      "entry":[
        {
          "id":"PAGE_ID",
          "time":1460245674269,
          "messaging":[
            {
              "sender":{
                "id":"12345"
             },
              "recipient":{
                "id":"10"
             },
              "timestamp":1460245672080,
              "message":{
                "mid":"mid.1460245671959:dad2ec9421b03d6f78",
                "seq":216,
                "text":"Hi"
              }
            }
          ]
        }
      ]
    }''',
    '''{
      "object":"page",
      "entry":[
        {
          "id":"PAGE_ID",
          "time":1460245674269,
          "messaging":[
            {
              "sender":{
                "id":"12345"
             },
              "recipient":{
                "id":"10"
             },
              "timestamp":1460245672080,
              "message":{
                "mid":"mid.1460245671959:dad2ec9421b03d6f78",
                "seq":216,
                "text":"Good!"
              }
            }
          ]
        }
      ]
    }''']
