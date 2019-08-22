# thanks to Casper for contributing commands to this.


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



def findNthToken(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        print("yeah? %(n)d")
        Key("s-enter:%(n)d").execute()
    else:
        Key("enter:%(n)d").execute()
        print("no? %(n)d")
    Key('escape').execute()


class NOTvscodeCcrRule(MergeRule):
  
    mwith = CCRMerger.CORE

    mapping = {
    "jack [<n>] [<text>]": R(Key("cs-left:%(n)s, del") + Text("%(text)s")),
    "mack [<n>] [<text>]": R(Key("c-left:%(n)s") + Text("%(text)s")),
        
    "jill [<n>]": R(Key("cs-right:%(n)s, del") + Text("%(text)s")),
    "dack [<n>] [<text>]": R(Key("c-right:%(n)s") + Text("%(text)s")),

    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 100),
        # IntegerRefST("m", 1, 1000),
        Choice("parable_character", {
            "sarens": "lparen", # parentheses noninclusive
            "eyesar": "rparen", # parentheses inclusive
            "swingle": "squote", # single quotes
            "dwingle": "dquote", # double quotes
            "swacket": "lbracket", # square brackets inclusive
            "swirly": "lbrace", # curly braces inclusive
            "sangy": "langle", # angle brackets inclusive 
        }),

                ]
        
    defaults = {"n": 1, "mim": "", "text": ""}



#---------------------------------------------------------------------------

# Initialise the rule.
ccr_rule_1 = NOTvscodeCcrRule()
context = ~AppContext(executable="code")

# Add VisualStudioCodeCcrRule as a caster Ccr app rule. (at least I think that's what this does )
control.nexus().merger.add_app_rule(ccr_rule_1, context)
#control.nexus().merger.add_app_rule(ccr_rule_2, context)

