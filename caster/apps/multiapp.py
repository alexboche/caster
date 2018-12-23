import dragonfly
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

from . import utils


class AnkiWordRule(MergeRule):

    mapping = {
        "add": R(Key("a"), rdescript="Multi: Add"),
        "adder": R(Key("b")),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
    ]
    defaults = {"n": 1, "dict": "nothing"}


grammar = Grammar("anki_word", context=utils.MultiAppContext(relevant_apps={'anki', 'word'}))

if settings.SETTINGS["apps"]["multi"]:
        rule = AnkiWordRule(name="multi")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
