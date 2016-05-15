from database.sampledata                               import Sampledata
from database.db                                       import Db
from datetime                                          import time, tzinfo, datetime, timedelta
import datetime as dt
import time
import re
import logging, sys

class ResponseBuilder:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO) # INFO, WARNING OR DEBUG
    db = Db()
    messages = db.getMessages()
    conversations = db.getConversations()
    resetmsg = 'chatreset'
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
    # matches any of the user-programmed input
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
        return matches


    def isFirstQuestion(self, question):
        m_nrs = self.getm_nrsForConvId(question['conv_id'])
        try:
            return question['m_nr'] == m_nrs[0]
        except Exception, e:
            print 'isFirstQuestion fail:', e
            return False


    def isUserRegisteredInConversationState(self, messageSender):
        return (messageSender in self.conversationstates)


    # Logic from hell. Needs refactoring terribly!
    # Because of is_alternative messages, checking whether a sent message is a
    # follow up of the previously sent msg can be tricky.
    # From a set of is_alternatives, only 1 of them should be said. Example
    # below: After saying m_nr 1, m_nr 3 is aFollowUpQuestion. But, m_nr 2 is
    # as well. But, m_nr 3 is not a follow up of m_nr 2.
    # Additionally, m_nr 4 is a follow up of both m_nr 2 and m_nr 3
    #
    #  { "m_nr" : 1, "qtext" : "Hi", "is_alternative" : False, ... },
    #  { "m_nr" : 2, "qtext" : "Good!", "is_alternative" : True, ... },
    #  { "m_nr" : 3, "qtext" : "Bad!", is_alternative" : True, ...}
    #  { "m_nr" : 4, "qtext" : "You?", "is_alternative" : False, ...}
    #
    def isFollowUpQuestion(self, messageSender, question):
        sortedm_nrs = self.getm_nrsForConvId(question['conv_id'])
        m_nrs_isalternatives = self.getm_nrsAndis_alternativeForConvId(question['conv_id'])

        mostrecentquestion = self.getSendersMostRecentQuestionForConvId(messageSender, question['conv_id'])
        if not mostrecentquestion:
            return False

        indexMostRecentQuestion = sortedm_nrs.index(mostrecentquestion)
        indexAskedQuestion = sortedm_nrs.index(question['m_nr'])

        if indexMostRecentQuestion >= indexAskedQuestion:
            return False

        isDirectFollowUp = self.isDirectFollowUpQuestion(sortedm_nrs, mostrecentquestion, question['m_nr'])
        if isDirectFollowUp:
            isMostRecentQAlternative = m_nrs_isalternatives[mostrecentquestion] #self.isMostRecentQuestionAlternative(mostrecentquestion, question['conv_id'])
            if isMostRecentQAlternative:
                if question['is_alternative']:
                    return False
                else:
                    return True
            else:
                return True
        else:
            indexCheckQuestion = indexAskedQuestion - 1
            # LOGIC can be refactored. While loop happens in both conditions,
            # reduce to once then check condition?
            if question['is_alternative']:
                while indexMostRecentQuestion > indexCheckQuestion:
                    if m_nrs_isalternatives[indexCheckQuestion]:
                        indexCheckQuestion -= 1
                        continue
                    else:
                        return False
                if m_nrs_isalternatives[mostrecentquestion]:
                    return False
                else:
                    return True
            else:
                while indexMostRecentQuestion > indexCheckQuestion:
                    if m_nrs_isalternatives[indexCheckQuestion]:
                        indexCheckQuestion -= 1
                        continue
                    else:
                        return False
                if m_nrs_isalternatives[mostrecentquestion]:
                    return True
                else:
                    return False





    def getSendersMostRecentQuestionForConvId(self, messageSender, conv_id):
        if self.isUserRegisteredInConversationState(messageSender):
            mostrecentquestion = 0
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == conv_id:
                    return convstate['mostrecentquestion']
        else:
            return False


    # For when mostrecentquestion = 2, and asked m_nr = 3.
    # Will also work when m_nr 3 has been removed, mostrecentquestion = 2,
    # and m_nr = 4
    def isDirectFollowUpQuestion(self, sortedm_nrs, mostrecentquestion, m_nr):
        try:
            indexMostRecentQuestion = sortedm_nrs.index(mostrecentquestion)
            indexAskedQuestion = sortedm_nrs.index(m_nr)
            print 'direct follow up:', indexAskedQuestion == indexMostRecentQuestion + 1
            return indexAskedQuestion == indexMostRecentQuestion + 1
        except ValueError:
            return False



    # def isMostRecentQuestionAlternative(self, mostrecentquestion, conv_id):
    #     for message in self.messages:
    #         if message['conv_id'] == conv_id & message['m_nr'] == mostrecentquestion:
    #             print 'match gevonden'
    #             return message



        # m_nrs = self.getm_nrsAndis_alternativeForConvId(question['conv_id'])
        # try:
        #     for convstate in self.conversationstates[messageSender]:
        #         if convstate['conv_id'] == question['conv_id']:
        #             if question['m_nr'] == (convstate['mostrecentquestion'] + 1):
        #                 return True
        #             else:
        #                 return True
        #                 # arePrevMessagesAlternatives = self.arePreviousMessagesAlternatives(question['m_nr'], convstate['mostrecentquestion'], m_nrs)
        #                 # if (arePrevMessagesAlternatives):
        #                 #     return self.hasAlternativeQuestionBeenAsked(question['m_nr'], m_nrs)
        #                 # else:
        #                 #     return False
        # except Exception, e:
        #     print 'exception, probably indexerror ', e
        #     return False
        # return False


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
    def arePreviousMessagesAlternatives(this, m_nr, mostrecentquestion, m_nrs_isalternatives):
        print 'm_nr:', m_nr, 'mrquestion:', mostrecentquestion, 'm_nrisalts:', m_nrs_isalternatives
        # TODO Problem 1: you can go from 1 to 4 and skip all is_alternatives
        previousMsgsAreAlternatives = False

        if m_nr <= mostrecentquestion:
            return False

        currentMessage = m_nr-1
        while currentMessage > mostrecentquestion:
            try:
                if m_nrs_isalternatives[currentMessage] == True:
                    currentMessage -= 1
                    previousMsgsAreAlternatives = True
                    continue
                else:
                    print 'previous msg was not isalternative True, not a follow up:', currentMessage, ' - ', m_nrs_isalternatives[currentMessage-1]
                    return False
            except Exception, e:
                print 'probably indexerror in arePreviousMessagesAlternatives:', e
        print 'all previous messages are is_alternative, its a follow up!', previousMsgsAreAlternatives

        return previousMsgsAreAlternatives


    # tests if at least one of the previous 'is_alternative' questions have
    # been asked. if not, they were skipped and the example m_nr: 1 -> m_nr:4
    # will return an unwarranted response
    def hasAlternativeQuestionBeenAsked(this, m_nr, m_nrs_isalternatives):
        print 'checking if alt questions have been asked'
        return m_nrs_isalternatives[m_nr]


    def getm_nrsAndis_alternativeForConvId(self, conv_id):
        m_nrs = {}
        for msg in self.messages:
            if conv_id == msg['conv_id']:
                m_nrs[msg['m_nr']] =  msg['is_alternative']
        return m_nrs


    def getm_nrsForConvId(self, conv_id):
        m_nrs = []
        for msg in self.messages:
            if msg['conv_id'] == conv_id:
                m_nrs.append(msg['m_nr'])
        return sorted(m_nrs)


    def hasConversationTimedOut(self, messageSender, question):
        try:
            for convstate in self.conversationstates[messageSender]:
                if convstate['conv_id'] == question['conv_id']:
                    currenttime = datetime.utcnow()
                    return ((currenttime - convstate['mostrecentinteraction']) > self.conversationTimeoutThreshold)
        except Exception, e:
            print 'exception:', e
            return False
        return False


    # Logic of doom to check if a question requires a response
    # probably better with switch statement
    def shouldGetResponse(self, isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut):
        logging.info([isFirstQuestion, isUserRegisteredInConversationState, isFollowUpQuestion, hasConversationTimedOut])
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
            'mostrecentinteraction' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']})
            return True
        # First registration of record for messageSender
        else:
            self.conversationstates[messageSender] = [{'conv_id' : question['conv_id'],
            'mostrecentinteraction' : datetime.utcnow(), 'mostrecentquestion': question['m_nr']}]
            return True


    def resetSendersConversationState(self, messageSender):
        try:
            self.conversationstates[messageSender] = []
        except Exception, e:
            logging.info('User did not have conversationstate to reset')
            return False


    def reinitialize(self, messageSender):
        logging.info('Resetting. Fetching questions and responses from DB...')
        self.messages = self.db.getMessages()
        self.resetSendersConversationState(messageSender)


    def replaceEscapedCharacters(self, message):
      escapedMessage = self.escapeTextPattern(message, '$', '&#36;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '<', '&#60')
      escapedMessage = self.escapeTextPattern(escapedMessage, '>', '&#62;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '\'', '&#39;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '\"', '&#34;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '\\', '&#92;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '\/', '&#47;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '[', '&#91;')
      print '\n## the escaped msg:', escapedMessage
      return escapedMessage


    def escapeTextPattern(self, input, pattern, replacewith):
        return input.replace(pattern, replacewith)


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
            self.reinitialize(messageSender)

        message = self.replaceEscapedCharacters(message)

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
                print 'shouldGetResponseBool:', shouldGetResponseBool
                if shouldGetResponseBool:
                    print 'shud get response'
                    response = question['rtext']
                    isConvStateUpdated = self.updateConversationState(messageSender, question)
                    print 'response: ', response, '\n conv state updated: ', isConvStateUpdated, '\n'
                    returnResponses.append({'responseText' : response})
                else:
                    print 'shud not get response'
        print returnResponses
        return returnResponses
