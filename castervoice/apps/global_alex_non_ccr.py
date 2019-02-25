#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
global

"""
# ---------------------------------------------------------------------------
from inspect import getargspec

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




class GlobalRule(MergeRule):
    pronunciation = "global"

    mapping = {


    }
    extras = [
        Choice("click_by_voice_options", {
            "go": "f",
            "click": "c",
            "push": "b",
            "otab": "t",
            "window": "w",
            "hover": "h",
            "link": "k",
            "copy": "s",
        }),
        Dictation("dictation"),
        IntegerRefST("n", 1, 10),
        IntegerRefST("m", 1, 10),
        IntegerRefST("numbers", 1, 1000),

    ]
    defaults = {"n": 1, "dict": "", "click_by_voice_options": "c"}


# ---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=context)

if settings.SETTINGS["apps"]["chrome"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(GlobalRule())
    else:
        rule = GlobalRule(name="chrome") # fill this in
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
