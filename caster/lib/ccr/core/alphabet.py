from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat, Function, Choice)

from caster.lib import control, alphanumeric
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class Alphabet(MergeRule):
    pronunciation = CCRMerger.CORE[0]

    mapping = {
        "[<big>] <letter>":
            R(Function(alphanumeric.letters2, extra={"big", "letter"}),
              rdescript="Spell"),
        # "word number <wn>":	
        #     R(Function(alphanumeric.word_numxber, extra="wn"), rdescript="Number As Word"),
	
        "numb <wnKK>":
            R(Function(alphanumeric.numbers2, extra="wnKK"),
              rspec="number",
          rdescript="Number"),
        "<symbol>": R(Text("\%(symbol)s") + Key("space"))  
	
    }
    extras = [
        alphanumeric.get_alphabet_choice("letter"),
        Choice("big", {
            "big": True,
        }),
        
        IntegerRefST("wn", 0, 10),	
        IntegerRefST("wnKK", 0, 1000000),
        Choice(
            "symbol",
            {
                "root": "sqrt",
                "integral": "int",
                "fraction": "frac",
                "alpha": "alpha",
                "beater": "beta",
                "gamma": "gamma",
                "delta": "delta",
                "epsilon": "epsilon",
                "zita": "zeta",
                "eater": "eta",
                "theta": "theta",
                "iota": "iota",
                "kappa": "kappa",
                "lambda": "lambda",
                "mu": "mu",
                "new": "nu",
                "zee": "xi",
                "pie": "pi",
                "row": "rho",
                "sigma": "sigma",
                "tau": "tau",
                "upsilon": "upsilon",
                "phi": "phi",
                "chi": "chi",
                "sigh": "psi",
                "omega": "omega",
                #
                "times": "times",
                "divide": "div",
                "intersection": "cap",
                "union": "cup",
                "stop": "cdot",
                "approximate": "approx",
                "proportional": "propto",
                "not equal": "neq",
                "member": "in",
                "for all": "forall",
                "partial": "partial",
                "infinity": "infty",
                "dots": "dots",
                #
                "left arrow": "leftarrow",
                "right arrow": "rightarrow",
                "up arrow": "uparrow",
                "down arrow": "downarrow",
                #
                "left": "left(",
                "right": "right)",
            }),
    ]
    defaults = {
        "big": False,
    }


control.nexus().merger.add_global_rule(Alphabet())
