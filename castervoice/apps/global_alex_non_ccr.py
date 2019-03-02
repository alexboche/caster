#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""


"""
#---------------------------------------------------------------------------
from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat, Choice, Function, ActionBase, ActionError, Playback, Mimic, Pause, WaitWindow)


from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text, Mouse
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
        "shesk": Key("w-d"),
        "eck": Key("escape"),
        #"swap": Key("win:down, f9, win:up"),
        "snarles": Text("hAtdickbootstorew8ght973"),
        "close": Key("a-f4"),
        "task manager": Key("cs-escape"),
        "find [<dict>]": Key("c-f") + Text("%(dict)s"),
        "(display | change display)": Key("w-d/10") + Mouse("[0.9, 0.5], right") + Key("up:2, enter/30, tab:2"),
        "troppy": Key("tab, a-down"), # this tas to and then drops down a drop-down list
        "droppy": Key("a-down"), # drops down a drop-down list
        #"clicker <m> [<wait_time>]": Mouse("left:%(m)s/%(wait_time)s"),
        "clicker": Mouse("left") * Repeat(count=8),

        "vocab": Playback([(["start", "vocabulary", "editor"], 0.03)]) * Repeat(extra="n"),
        "mimic recognition <dict> [<n> times]":
                    Mimic(extra="dict") * Repeat(extra="n"),
        "bocker": Mimic("dictation", "box"),
        
        "next group [<n>]": Key("w-backtick") * Repeat(extra='n'), # for groupy

        "save": Key("c-s"),
        "open": Key("c-o"),
        "print": Key("c-p"),
        "max": Key("a-space/15, x")
        

        

        # duplicate/extend display
        # click repetition command
        # google that
        # duck duck oh that

        
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),


    ]

    defaults = {"n": 1, "m": 1, "dict": "nothing"}

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
