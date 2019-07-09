


from dragonfly import (Grammar, Context, AppContext, Dictation, Repeat, Function, Choice, Mouse, Pause)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger


Curl = Key("lbrace, rbrace, left")

class TexMakerCcrRule(MergeRule):
    #pronunciation = "visual studio code continuous"
    mwith = CCRMerger.CORE

    mapping = {
        "dollz": Key("dollar:2, left"),        
        "double doll": Key("dollar:4, left:2"),
        "document class": Text("\\documentclass") + Curl + Text("article") + Key("end, enter"),
        "begin": Text("\\begin") + Curl + Text("document") + Key("enter"),
        "compile": Mouse("[401, 138], left") + Mouse("[0.4, 0.4], left"),
        
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 100),
        

                ]
        
    defaults = {"n": 1, "mim": "", "text": ""}

# class DictationNonCcrRule(MergeRule):
#     pronunciation = "Visual Studio code non-continuous"
#     mapping = {
        
        
       
#         "new file": R(Key("c-n"), rdescript="new file"),
       
       
       
       
       


#     }
#     extras = [
#         Dictation("text"),
#         Dictation("mim"),
#         IntegerRefST("n", 1, 1000),
#         Choice("first_second_third", {
#                 "first": "1",
#                 "second": "2",
#                 "third": "3",
#                 "fourth": "4",
#                 "fifth": "5",
#                 "sixth": "6",
#             }),
        
#     ]
#     defaults = {"n": 1, "mim": "", "text": ""}


#---------------------------------------------------------------------------

# Initialise the rule.
ccr_rule_1 = TexMakerCcrRule()

#non_ccr_rule = VisualStudioCodeNonCcrRule()



context = AppContext(executable="texmaker")

# Add VisualStudioCodeCcrRule as a caster Ccr app rule. (at least I think that's what this does )
control.nexus().merger.add_app_rule(ccr_rule_1, context)



# grammar = Grammar("code", context=context)

# grammar.add_rule(non_ccr_rule)
# grammar.load()


