#!/usr/bin/python

class Sampledata:

    def getConversations(self):
        return self.convs

    def getTestconversationState(self):
        return self.testconversationstate

    def getMessages(self):
        return self.messages

    convs = [
        { "conv_id" : 1, "conv_name" : "example chat"},
        { "conv_id" : 2, "conv_name" : "second chat"},
        # { "conv_id" : 3, "conv_name" : "third chat"}
    ]

    messages = [
     { "m_nr" : 1, "qtext" : "Hi", "rtext" : "Hi! :) How are you?", "is_alternative" : False, "conv_id" : 1, "key" : 123 },
     { "m_nr" : 2, "qtext" : "Good!", "rtext" : "That's great to hear!", "is_alternative" : True, "conv_id" : 1, "key" : 124 },
     { "m_nr" : 3, "qtext" : "Bad!", "rtext" : "I'm sorry to hear that", "is_alternative" : True, "conv_id" : 1, "key" : 125 },
     { "m_nr" : 4, "qtext" : "OK", "rtext" : "nice", "is_alternative" : True, "conv_id" : 1, "key" : 126 },
     { "m_nr" : 5, "qtext" : "How about you?", "rtext" : "I'm doing just fine!", "is_alternative" : False, "conv_id" : 1, "key" : 127 },
     { "m_nr" : 1, "qtext" : "Food", "rtext" : "Can I order you anything?", "is_alternative" : False, "conv_id" : 2, "key" : 128 },
     { "m_nr" : 2, "qtext" : "Pizza", "rtext" : "Ordering you a pizza as we speak!", "is_alternative" : True, "conv_id" : 2, "key" : 129 },
     { "m_nr" : 3, "qtext" : "Burrito", "rtext" : "Ordering you a burrito as we speak!", "is_alternative" : True, "conv_id" : 2, "key" : 130 },
    ]



    testconversationstate = {
        123 : [
            {'conv_id': 1, 'latestinteraction' : 10, 'mostrecentquestion': 2.2 },
            {'conv_id': 2, 'latestinteraction' : 30, 'mostrecentquestion': 2 },
        ],
        456 : [
            {'conv_id': 2, 'latestinteraction' : 44, 'mostrecentquestion': 1 },
            {'conv_id': 3, 'latestinteraction' : 30, 'mostrecentquestion': 5 },
            {'conv_id': 1, 'latestinteraction' : 2, 'mostrecentquestion': 3 },
        ],
        789 : [
            {'conv_id': 5, 'latestinteraction' : 21, 'mostrecentquestion': 1 },
            {'conv_id': 4, 'latestinteraction' : 30, 'mostrecentquestion': 1 },
            {'conv_id': 1, 'latestinteraction' : 2, 'mostrecentquestion': 3 },
        ]
    }
