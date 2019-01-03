from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice)

from caster.lib import control, alphanumeric
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.apps import utils


def symbol_letters(big, symbol):
    if big:
        symbol = symbol.title()
    Text(str(symbol)).execute()


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
        # "<symbol>":
        #     R(Text("\%(symbol)s") + Key("space")),
        # # "[<big>] <greekletter>":
        #     R(Function(symbol_letters, extra={"big", "greekletter"}),
        #         rdescript="potentially capitalized greek letters"),
        "[<big>] <symbol>":
            R(Text("\\") + Function(symbol_letters, extra={"big", "symbol"}) + Text(" "),
              rdescript="LaTeX: Insert symbols"),
        "smath": Key("c-m"), 
    
            }

    extras = [
        alphanumeric.get_alphabet_choice("letter"),
        Choice("big", {
            "big": True,
        }),
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
        # Choice(
        #     "greekletter", {
        #         "alpha": "alpha",
        #         "beater": "beta",
        #         "gamma": "gamma",
        #         "delta": "delta",
        #         "epsilon": "epsilon",
        #         "zita": "zeta",
        #         "eater": "eta",
        #         "theta": "theta",
        #         "iota": "iota",
        #         "kappa": "kappa",
        #         "lambda": "lambda",
        #         "mu": "mu",
        #         "new": "nu",
        #         "zee": "xi",
        #         "cherry": "pi",
        #         "row": "rho",
        #         "sigma": "sigma",
        #         "tau": "tau",
        #         "upsilon": "upsilon",
        #         "phi": "phi",
        #         "chi": "chi",
        #         "sigh": "psi",
        #         "omega": "omega",
        #     }),
        Choice(
            "symbol",
            {
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
                "cherry": "pi",
                "row": "rho",
                "sigma": "sigma",
                "tau": "tau",
                "upsilon": "upsilon",
                "phi": "phi",
                "chi": "chi",
                "sigh": "psi",
                "omega": "omega",
                
                
                # operators
                "root": "sqrt",
                "generic root": "root",
                "integ": "int",
                "double integ": "iint",
                "triple integ": "iiint",
                "times": "times",
                "divide": "div",
                "intersection": "cap",
                "union": "cup",
                "stop": "cdot",
                "sum": "sum",
                "product": "prod",
                "(direct sum | oh plus)": "oplus",
                "(large direct sum | large oh plus)": "bigoplus",
                "plus or minus": "pm",


                

                # fractions and related things in the lyx fractions menu
                "frac": "frac",
                "(nice frack | nice fraction)": "nicefrac",
                "unit": "unitone",
                "unit two": "unittwo",
                "unit fraction ": "unitfrac",
                "text fraction": "tfrac",
                "display fraction": "dfrac",
                "continued fraction": "cfrac",
                "continued fraction (left)": "cfracleft",
                "continued fraction (right)": "cfracright",
                "binomial": "binom",
                "text binomial": "tbinom",
                "display binomial": "dbinom",

                # functions
                "arccoase": "arccos",
                "arcsine": "arcsin",
                "arctan": "arctan",
                "arg": "arg",
                "beemod": "bmod",  ## i'm not familiar with this one
                "coase": "cos",
                "kosh": "cosh",
                "hyperbolic tangent": "cot",
                "hyperbolic cotangent": "coth",
                "cosecant": "csc",
                "degree": "deg",
                "determinant": "det",
                "dimension": "dim",
                "exp": "exp",
                "GCD": "gcd",
                "cat hom": "hom",
                "infimum": "inf",
                "kernel": "ker",
                "limit": "lim",
                "liminf": "liminf",
                "LN": "ln",
                "log": "log",
                "max": "max",
                "min": "min",
                "secant": "sec",
                "sine": "sin",
                "sinch": "sinh",
                "supremum": "sup",
                "tangent": "tan",
                "tanch": "tanh",
                "prob": "Pr",







                # relations
                "subset": "subset", 
                "superset": "supset",
                "strict subset": "subsetneq",
                "strict superset": "supsetneq",
                "preck": "prec",
                "preck equals": "preceq",
                "suck": "succ",
                "suck equals": "succeq",
                "approximate": "approx",
                "proportional": "propto",
                "not equal": "neq",
                "geequal": "geq", 
                "leaqual": "leq",
                "member": "in",

                "partial": "partial",
                "infinity": "infty",
                "dots": "dots",
                
                # logic
                "(land|logic and)": "land", 
                "logic or": "lor",
                "primer": "prime",
                "logic not": "lnot", 
                "for all": "forall",
                "there exists": "exists", 

                # math fonts
                "(beebee|blackboard bold)": "mathbb",
                "roman": "mathrm",
                "bold": "mathbf",
                "bold symbol": "boldsymbol",
                "sans serif": "mathsf",
                "italic": "mathit",
                "typewriter": "matttt",
                "blackboard": "mathbb",
                "fraktur": "mathfrak",
                "calligraphic": "mathcal",
                "formal script": "mathscr",
                "normal text mode": "textrm",






                #
                "left arrow": "leftarrow",
                "right arrow": "rightarrow",
                "up arrow": "uparrow",
                "down arrow": "downarrow",
                "left right arrow": "leftrightarrow",
                #
                "left": "left(",
                "right": "right)",
            }),
    ]
    defaults = {
        "big": False,
    }


control.nexus().merger.add_global_rule(Alphabet())
