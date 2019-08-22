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


class AnkiRule(MergeRule):
    pronunciation = "anki"

    mapping = {
        "add": R(Key("a"), rdescript="Anki: Add"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------




context = utils.MultiAppContext(relevant_apps={'anki', 'winword'})
grammar = Grammar("anki", context=context)

if settings.SETTINGS["apps"]["anki"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AnkiRule())
    else:
        rule = AnkiRule(name="anki")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
