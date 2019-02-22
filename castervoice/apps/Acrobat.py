#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for word

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R



class AcrobatRule(MergeRule):
    pronunciation = "acrobat"

    mapping = {

        "benjamin [<n>]": R(Key('a/20')) * Repeat(extra='n'),
        #"go to pager [<n>]": R(Key("a-v, an, g/50")+nNotNull(""), rdescript="go to page acrobat)"),
        "open": R(Key("c-o")),
        "nindow":R(Key("a-w,n/40,ws-left"))
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="acrobat")
grammar = Grammar("acrobat", context=context)

if settings.SETTINGS["apps"]["acrobat"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(MSWordRule())
    else:
        rule = AcrobatRule(name="acrobat")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
