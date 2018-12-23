import dragonfly
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

from . import utils


class AnyAppRule(MergeRule):
   

    mapping = {
        "red blue": R(Text("purple"), rdescript="red blue"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
    ]
    defaults = {"n": 1, "dict": "nothing"}




context = utils.AnyAppContext()
grammar = Grammar("global_rule", context=context)

if settings.SETTINGS["apps"]["anyapp"]:
        rule = AnyAppRule(name="anyapp")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
