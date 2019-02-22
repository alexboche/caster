import dragonfly
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text,
                       Repeat, Function, Choice)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

from . import utils
from . import reloader
import io
import toml


# load the toml file
with io.open("C:\NatLink\NatLink\MacroSystem\caster\lib\ccr\core\math_vocab.toml") as f:
        math_vocab_list_of_dicts = toml.load(f)

full_math_vocab_dict = math_vocab_list_of_dicts[1]["full_math_vocab"]
math_vocab_with_subdicts = math_vocab_list_of_dicts[0]

# example of using subdict
logic_vocab = math_vocab_with_subdicts["logic"]

# format vocab for Lyx
lyx_full_math_vocab_dict = {k:"\\{} ".format(full_math_vocab_dict[k]) for k in full_math_vocab_dict}
        
class AnyAppRule(MergeRule):
    #  red blue red bluered blueregular red bluepurple
    #  red blue red blueorangered blue and blue
    mapping = {
        "red blue": R(Text("orange"), rdescript="red blue"),
        "reload grammars": R(Function(reloader.reload_app_grammars)),
        "save reload": R(Key("c-s") + Function(reloader.reload_app_grammars)),
        "satch [<n>]": Key("alt:down, tab/20:%(n)d, alt:up"),
        # "soap": R(Playback([(["switch"], 0.0)])), {.}early numb 5,
        # "num <n2>": R(Text("%(n2)d")),
        "<symbol_1>": R(Text("%(symbol_1)s")),
        
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
        IntegerRefST("n2", 1, 10),
        Choice("symbol_1", lyx_full_math_vocab_dict),
            ]
    defaults = {"n": 1, "dict": "nothing"}


context = utils.AnyAppContext()
grammar = Grammar("global_rule", context=context)

if settings.SETTINGS["apps"]["anyapp"]:
        rule = AnyAppRule(name="anyapp")
        
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
