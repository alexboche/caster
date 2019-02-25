#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""


"""
#---------------------------------------------------------------------------
from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat, Choice, Function, ActionBase, ActionError)


from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils
from castervoice.apps import reloader
from castervoice.apps import reloader


class GlobalAlexNonCcrRule(MergeRule):
    pronunciation = "global alex rule"

    mapping = {
        "red blue": R(Text("orange"), rdescript="red blue"),
        "reload grammars": R(Function(reloader.reload_app_grammars)),
        "save reload": R(Key("c-s") + Function(reloader.reload_app_grammars)),
        "satch [<n>]": Key("alt:down, tab/20:%(n)d, alt:up"),
               
        "<dict> (Peru)": Text(''),
        "(talk | talking) <dict>": Text(''),
        "<dict> (Brazil)": Key('f1'),

        
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),

    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------




context = utils.MultiAppContext(relevant_apps={})
grammar = Grammar("global_alex_non_ccr", context=context)

if settings.SETTINGS["apps"]["global_alex_non_ccr"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(GlobalAlexNonCcrRule())
    else:
        rule = GlobalAlexNonCcrRule(name="global_alex_non_ccr")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
