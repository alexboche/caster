# NatLink macro definitions for NaturallySpeaking
# coding: latin-1
# Generated by vcl2py 2.8.6, Sat Dec 22 17:06:02 2018

import natlink
from natlinkutils import *
from VocolaUtils import *


class ThisGrammar(GrammarBase):

    gramSpec = """
        <dgndictation> imported;
        <cbvo> = ('focus' | 'click' | 'new tab' ) ;
        <1> = 'duplicate tab' ;
        <2> = 'duplicate window' ;
        <3> = 'add site' <dgndictation> ;
        <4> = 'add site' ;
        <any> = <1>|<2>|<3>|<4>;
        <sequence> exported = <any> [<any> [<any> [<any>]]];
    """
    
    def initialize(self):
        self.load(self.gramSpec)
        self.currentModule = ("","",0)
        self.rule_state = {}
    
    def activate_rule(self, rule, window, status):
        current = self.rule_state.get(rule)
        active = (current == window)
        if status == active: return
        if current:
            self.deactivate(rule)
            self.rule_state[rule] = None
        if status:
            try:
                self.activate(rule, window)
                self.rule_state[rule] = window
            except natlink.BadWindow:
                pass

    def gotBegin(self,moduleInfo):
        self.firstWord = 0
        # Return if wrong application
        window = matchWindow(moduleInfo,'chrome','')
        if not window: return None
        # Return if same window and title as before
        if moduleInfo == self.currentModule: return None
        self.currentModule = moduleInfo

        title = string.lower(moduleInfo[1])
        self.activate_rule('sequence', moduleInfo[2], True)

    def convert_number_word(self, word):
        if   word == 'zero':
            return '0'
        elif word == 'one':
            return '1'
        elif word == 'two':
            return '2'
        elif word == 'three':
            return '3'
        elif word == 'four':
            return '4'
        elif word == 'five':
            return '5'
        elif word == 'six':
            return '6'
        elif word == 'seven':
            return '7'
        elif word == 'eight':
            return '8'
        elif word == 'nine':
            return '9'
        else:
            return word

    def get_cbvo(self, list_buffer, functional, word):
        if word == 'focus':
            list_buffer += 'f'
        elif word == 'click':
            list_buffer += 'c'
        elif word == 'new tab':
            list_buffer += 't'
        return list_buffer

    # 'duplicate tab'
    def gotResults_1(self, words, fullResults):
        if self.firstWord<0:
            return
        try:
            top_buffer = ''
            top_buffer += '{alt+d}'
            top_buffer += '{ctrl+c}'
            top_buffer += '{ctrl+t}'
            top_buffer += '{ctrl+v}'
            top_buffer += '{enter}'
            top_buffer = do_flush(False, top_buffer);
            self.firstWord += 1
            if len(words) > 1: self.gotResults_1(words[1:], fullResults)
        except Exception, e:
            handle_error('chrome.vcl', 10, '\'duplicate tab\'', e)
            self.firstWord = -1

    # 'duplicate window'
    def gotResults_2(self, words, fullResults):
        if self.firstWord<0:
            return
        try:
            top_buffer = ''
            top_buffer += '{alt+d}'
            top_buffer += '{ctrl+c}'
            top_buffer += '{ctrl+n}'
            top_buffer += '{ctrl+v}'
            top_buffer = do_flush(False, top_buffer);
            unimacro_arg1 = ''
            unimacro_arg1 += 'WINKEY '
            unimacro_arg1 += 'shift+left'
            call_Unimacro(unimacro_arg1)
            top_buffer = do_flush(False, top_buffer);
            self.firstWord += 1
            if len(words) > 1: self.gotResults_2(words[1:], fullResults)
        except Exception, e:
            handle_error('chrome.vcl', 11, '\'duplicate window\'', e)
            self.firstWord = -1

    # 'add site' <_anything>
    def gotResults_3(self, words, fullResults):
        if self.firstWord<0:
            return
        fullResults = combineDictationWords(fullResults)
        opt = 1 + self.firstWord
        if opt >= len(fullResults) or fullResults[opt][1] != 'converted dgndictation':
            fullResults.insert(opt, ['', 'converted dgndictation'])
        try:
            top_buffer = ''
            top_buffer += '{alt+d}'
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += '50'
            saved_firstWord = self.firstWord
            call_Dragon('Wait', 'i', [dragon_arg1])
            self.firstWord = saved_firstWord
            top_buffer += '{ctrl+c}'
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += '100'
            saved_firstWord = self.firstWord
            call_Dragon('Wait', 'i', [dragon_arg1])
            self.firstWord = saved_firstWord
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += 'edit'
            dragon_arg2 = ''
            dragon_arg2 += 'folders'
            saved_firstWord = self.firstWord
            call_Dragon('HeardWord', 'ssssssss', [dragon_arg1, dragon_arg2])
            self.firstWord = saved_firstWord
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += '100'
            saved_firstWord = self.firstWord
            call_Dragon('Wait', 'i', [dragon_arg1])
            self.firstWord = saved_firstWord
            top_buffer += '{ctrl+end}'
            top_buffer += '{end}'
            top_buffer += '{enter}'
            top_buffer += '{ctrl+v}'
            top_buffer += '{home}'
            top_buffer += '{space}'
            top_buffer += '{left}'
            top_buffer += '='
            top_buffer += '{left}'
            top_buffer += '{space}'
            top_buffer += '{left}'
            when_value = ''
            word = fullResults[1 + self.firstWord][0]
            when_value += word
            if when_value != "":
                word = fullResults[1 + self.firstWord][0]
                top_buffer += word
                top_buffer = do_flush(False, top_buffer);
                dragon2_arg1 = ''
                dragon2_arg1 += '200'
                saved_firstWord = self.firstWord
                call_Dragon('Wait', 'i', [dragon2_arg1])
                self.firstWord = saved_firstWord
                top_buffer += '{ctrl+s}'
                top_buffer += '{alt+f4}'
            top_buffer = do_flush(False, top_buffer);
            self.firstWord += 2
        except Exception, e:
            handle_error('chrome.vcl', 14, '\'add site\' <_anything>', e)
            self.firstWord = -1

    # 'add site'
    def gotResults_4(self, words, fullResults):
        if self.firstWord<0:
            return
        try:
            top_buffer = ''
            top_buffer += '{alt+d}'
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += '50'
            saved_firstWord = self.firstWord
            call_Dragon('Wait', 'i', [dragon_arg1])
            self.firstWord = saved_firstWord
            top_buffer += '{ctrl+c}'
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += '100'
            saved_firstWord = self.firstWord
            call_Dragon('Wait', 'i', [dragon_arg1])
            self.firstWord = saved_firstWord
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += 'edit'
            dragon_arg2 = ''
            dragon_arg2 += 'folders'
            saved_firstWord = self.firstWord
            call_Dragon('HeardWord', 'ssssssss', [dragon_arg1, dragon_arg2])
            self.firstWord = saved_firstWord
            top_buffer = do_flush(False, top_buffer);
            dragon_arg1 = ''
            dragon_arg1 += '100'
            saved_firstWord = self.firstWord
            call_Dragon('Wait', 'i', [dragon_arg1])
            self.firstWord = saved_firstWord
            top_buffer += '{ctrl+end}'
            top_buffer += '{end}'
            top_buffer += '{enter}'
            top_buffer += '{ctrl+v}'
            top_buffer += '{home}'
            top_buffer += '{space}'
            top_buffer += '{left}'
            top_buffer += '='
            top_buffer += '{left}'
            top_buffer += '{space}'
            top_buffer += '{left}'
            when_value = ''
            when_value += ''
            if when_value != "":
                top_buffer += ''
                top_buffer = do_flush(False, top_buffer);
                dragon2_arg1 = ''
                dragon2_arg1 += '200'
                saved_firstWord = self.firstWord
                call_Dragon('Wait', 'i', [dragon2_arg1])
                self.firstWord = saved_firstWord
                top_buffer += '{ctrl+s}'
                top_buffer += '{alt+f4}'
            top_buffer = do_flush(False, top_buffer);
            self.firstWord += 1
            if len(words) > 1: self.gotResults_4(words[1:], fullResults)
        except Exception, e:
            handle_error('chrome.vcl', 14, '\'add site\'', e)
            self.firstWord = -1

thisGrammar = ThisGrammar()
thisGrammar.initialize()

def unload():
    global thisGrammar
    if thisGrammar: thisGrammar.unload()
    thisGrammar = None