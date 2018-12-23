# NatLink macro definitions for NaturallySpeaking
# coding: latin-1
# Generated by vcl2py 2.8.6, Sat Dec 22 17:06:02 2018

import natlink
from natlinkutils import *
from VocolaUtils import *


class ThisGrammar(GrammarBase):

    gramSpec = """
        <1> = 'test command' ;
        <2> = 'hello' ;
        <any> = <1>|<2>;
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
        window = matchWindow(moduleInfo,'wordpad','')
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

    # 'test command'
    def gotResults_1(self, words, fullResults):
        if self.firstWord<0:
            return
        try:
            top_buffer = ''
            top_buffer += 'success'
            top_buffer = do_flush(False, top_buffer);
            self.firstWord += 1
            if len(words) > 1: self.gotResults_1(words[1:], fullResults)
        except Exception, e:
            handle_error('wordpad.vcl', 4, '\'test command\'', e)
            self.firstWord = -1

    # 'hello'
    def gotResults_2(self, words, fullResults):
        if self.firstWord<0:
            return
        try:
            top_buffer = ''
            top_buffer += 'hello'
            top_buffer += 'world'
            top_buffer = do_flush(False, top_buffer);
            self.firstWord += 1
            if len(words) > 1: self.gotResults_2(words[1:], fullResults)
        except Exception, e:
            handle_error('wordpad.vcl', 5, '\'hello\'', e)
            self.firstWord = -1

thisGrammar = ThisGrammar()
thisGrammar.initialize()

def unload():
    global thisGrammar
    if thisGrammar: thisGrammar.unload()
    thisGrammar = None
