#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for word

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat, Choice)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R



class AcrobatRule(MergeRule):
    pronunciation = "acrobat"

    mapping = {

        "benjamin [<n>]": R(Key('a/20')) * Repeat(extra='n'),
        "pager [<n>]": R(Key("a-v, n, g/15") + Text("%(n)s") + Key("enter"),
            rdescript="go to page acrobat)"),
        "open": R(Key("c-o")),
        "nindow":R(Key("a-w,n/40,ws-left")),
        "enable scrolling": R(Key("a-v, p, c")),
        
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 1000),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="acrobat")
grammar = Grammar("acrobat", context=context)

if settings.SETTINGS["apps"]["acrobat"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AcrobatRule())
    else:
        rule = AcrobatRule(name="acrobat")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
