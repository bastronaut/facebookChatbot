from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re
import logging, sys

class ResponseBuilder:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING) # INFO, WARNING OR DEBUG
    db = Db()
    messages = db.getMessages()
    conversations = db.getConversations()
    resetmsg = 'reload'
    conversationTimeoutThreshold = dt.timedelta(seconds=10)

    # Keeps track of the state of different conversations, so different people
    # can talk to the bot at the same time without the chat intermingling a
    # response. messageEntity.getFrom() will be key.The most recent
    # interaction with the bot will be tracked to figure out if the conversation
    # has timed out and should be reset. Finally, it tracks how far into the
    # conversation they are.
    # conversationstates = {
    #     m.getFrom() : [
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}],
    #     m.getFrom() : [
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}],
    #     m.getFrom() : [
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
    #         {conv_id : x, mostrecentinteraction: timestamp, mostrecentquestion: question_nr}]
    # }
    #
    # messages: [
    #   { "m_nr" : 1, "qtext" : "hoi1", "rtext" : "doei 1", "is_alternative" : False, "conv_id" : 1, "key" : 123 },
    #        ..]

    conversationstates = {}

    # searces through self.messages to find if the incoming message
    # matches any of the preprogrammed input
    def findMessageQuestionMatches(self, incomingmessage):
        matches = []
        for message in self.messages:
            loweredmessage = message['qtext'].lower()
            if (re.search(r'\b' + loweredmessage + r'\b', incomingmessage)):
                # print '\n\nRE match, appending', loweredmessage, incomingmessage, re.search(r'\b' + loweredmessage + r'\b', incomingmessage)
                matches.append(message)
            elif loweredmessage == incomingmessage:
                # print 'exact match, appending', message
                matches.append(message)
        # print 'returning matches:', matches
        return matches


    def isFirstQuestion(self, question):
        return (question['m_nr'] == 1)


    def isUserRegisteredInConversationState(self, messageSender):
        return (messageSender in self.conversationstates)


    def isFollowUpQuestion(self, messageSender, question):
        m_nrs = self.getm_nrsAndis_alternativeForConvId(question['conv_id'])
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    if question['m_nr'] == (convstate['mostrecentquestion'] + 1):
                        return True
                    else:
                        return self.testPreviousMessagesAreAlternatives(question['m_nr'], convstate['mostrecentquestion'], m_nrs)
        except Exception, e:
            print 'exception, probably indexerror ', e
            return False
        return False


    # A message is a follow up question if the previous message is_alternative
    # are true. Simplified example below, the m_nr of the questionmatch is 3.
    # The m_nr before it, 2, have is_alternative set True. Continue until it
    # checks all previous questions until it finds the most recent question = 1.
    # Messages =
    #  { "m_nr" : 1, "qtext" : "Hi", "rtext": "how are you?", "is_alternative" : False },
    #  { "m_nr" : 2, "qtext" : "Good!", "rtext" : "Nice!", "is_alternative" : True },
    #  { "m_nr" : 3, "qtext" : "Bad!", "rtext" : "Too bad", "is_alternative" : True}
    #  { "m_nr" : 4, "qtext" : "You?", "rtext" : "Great!", "is_alternative" : False}
    # This only goes if the questionmatch has is_alternative itself. For example,
    # if the mostrecentquestion is 1, m_nr 4 will fail
    def testPreviousMessagesAreAlternatives(this, m_nr, mostrecentquestion, m_nrs_isalternatives):
        print 'm_nr:', m_nr, 'mrquestion:', mostrecentquestion, 'm_nrisalts:', m_nrs_isalternatives
        # if the questionmatch is is_alternative itself, follow up does not hold
        # see example above with m_nr = 4
        # TODO: FIX PROBLEM WITH LOGIC: you can go from 1 to 4 and skip all is_alternatives
        # if m_nrs_isalternatives[m_nr] == False:
        #     return False

        if m_nr <= mostrecentquestion:
            return False

        currentMessage = m_nr-1
        while currentMessage > mostrecentquestion:
            try:
                if m_nrs_isalternatives[currentMessage] == True:
                    currentMessage -= 1
                    continue
                else:
                    print 'previous msg was not isalternative True, not a follow up:', currentMessage, ' - ', m_nrs_isalternatives[currentMessage-1]
                    return False
            except Exception, e:
                print 'probably indexerror in testPreviousMessagesAreAlternatives:', e
        print 'all previous messages are is_alternative, its a follow up!'
        return True



    def getm_nrsAndis_alternativeForConvId(self, conv_id):
        m_nrs = {}
        for msg in self.messages:
            if conv_id == msg['conv_id']:
                m_nrs[msg['m_nr']] =  msg['is_alternative']
        return m_nrs


    def hasConversationTimedOut(self, messageSender, question):
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    currenttime = datetime.utcnow()
                    return (currenttime - convstate['mostrecentinteraction']) > self.conversationTimeoutThreshold
        except Exception, e:
            return False
        return False


    # Logic of doom to check if a question requires a response
    # probably better with switch statement
    def shouldGetResponse(self, isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut):
        # logging.info([isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut])
        if isFirstQuestion:
            if isUserRegisteredInConversationState:
                if hasConversationTimedOut:
                    return True
                else:
                    return False # TODO hmm, ask for a reset?
            else:
                return True
        else:
            if isUserRegisteredInConversationState:
                if isFollowUpQuestion:
                    return True
                else:
                    return False
            else:
                return False


    def updateConversationState(self, messageSender, question):
        if messageSender in self.conversationstates:
            for conversationstate in self.conversationstates[messageSender]:
                if conversationstate['conv_id'] == question['conv_id']:
                    conversationstate['mostrecentinteraction'] = datetime.utcnow()
                    conversationstate['mostrecentquestion'] = question['m_nr']
                    return True
            # The conversation_id conv_id had no record in the conv state yet, add it
            self.conversationstates[messageSender].append({'conv_id' : question['conv_id'],
            'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']})
            return True
        # First registration of record for messageSender
        else:
            self.conversationstates[messageSender] = [{'conv_id' : question['conv_id'],
            'timestamp' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']}]
            return True


    def resetSendersConversationState(self, messageSender):
        try:
            return(self.conversationstates.pop(messageSender, True))
        except Exception, e:
            logging.info('User did not have conversationstate to reset')
            return False


    def reinitialize(self):
        logging.info('Resetting. Fetching questions and responses from DB...')
        self.messages = db.getMessages()


    # Function entry point for class. Side effect for getting responses:
    # has to maintain a state of the current conversation. Probably not scaleable
    def getResponsesForMessage(self, messageEntity):
        returnResponses = []
        messageSender = messageEntity.getFrom()
        try:
            message = messageEntity.getBody().lower()
        except Exception, e:
            logging.info(['Fail getBody, probably different msg Type (e.g. media). Error: ', e])
            return returnResponses

        if message == self.resetmsg:
            self.reinitialize()



        questionmatches = self.findMessageQuestionMatches(message)
        # print '\nquestionmatches:\n', questionmatches
        if questionmatches:
            for question in questionmatches:
                shouldGetResponseBool = self.shouldGetResponse(
                self.isFirstQuestion(question),
                self.isUserRegisteredInConversationState(messageSender),
                self.isFollowUpQuestion(messageSender, question),
                self.hasConversationTimedOut(messageSender, question)
                )
                if shouldGetResponseBool:
                    response = question['rtext']
                    isConvStateUpdated = self.updateConversationState(messageSender, question)
                    print 'response: ', response, '\n conv state updated: ', isConvStateUpdated, '\n'
                    returnResponses.append({'responseText' : response})
        print returnResponses
        return returnResponses
