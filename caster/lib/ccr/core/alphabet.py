from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice)

from caster.lib import control, alphanumeric
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge.ccrmerger import CCRMerger
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R
from caster.apps import utils
from caster.lib.ccr.core import math_vocab


def symbol_letters(big, symbol):
    if big:
        symbol = symbol.title()
    Text(str(symbol)).execute()


def symbol_letters_small(symbol):
    Text(str(symbol)).execute()


def symbol_optional(symbol):
    #     Key("backslash").execute()
    #  Text("\\" + str(symbol) + " ").execute()

    Text(str(symbol)).execute()


def dummy(symbol):
    return symbol


def index_operator(index_operator, lower_limit, upper_limit, operand):
    pass


def latex_command(symbol):
    if symbol is None:
        return None
    return '\\{} '.format(symbol)

# \int _\alpha  ^\beta  





class Alphabet(MergeRule):
    pronunciation = CCRMerger.CORE[0]

    mapping = {
        "[<big_1>] <letter>":
            R(Function(alphanumeric.letters2, extra={"big_1", "letter"}),
              rdescript="Spell"),
        # "word number <wn>":
        #     R(Function(alphanumeric.word_numxber, extra="wn"), rdescript="Number As Word"),
        "numb <wnKK>":
            R(Function(alphanumeric.numbers2, extra="wnKK"),
              rspec="number",
              rdescript="Number"),
        "<index_operator> from <symbol_1> to <symbol_2> [<symbol_3>]":
            R(
                Text("\%(index_operator)s _") + Text("\%(symbol_1)s ") +
                Key("right, caret") + Text("\%(symbol_2)s ") +
                utils.ValueTexter(func=latex_command, extra={'symbol_3'}) + Key("right")),
        #"justice <symbol_1>": R(utils.Texter((dusquadmmy, extra={"symbol_1"})),
        # "justice": R(Text("\\")),
        # "hello <name>":
        #     R(Function(symbol_optional, extra={"name"})),

        # "<symbol_1> sub <symbol_2>": R(Text("\%(symbol_1)s _"
        # "<symbol_1> sub <symbol_2>": R(Text("") +
        #     Function(symbol_letters_small, extra={"symbol_1"}) + Text(" ") +
        #         Text("\%(symbol_2)s ")),
        # # "<symbol_1>":
        #     R(Text("\%(symbol_1)s") + Key("space")),
        # # # "[<big>] <greekletter>":
        #     R(Function(symbol_letters, extra={"big", "greekletter"}),
        #         rdescript="potentially capitalized greek letters"),
        # "[<big_1>] <symbol_1>":
        #     R(Text("\\") + Function(symbol_letters, extra={"big_1", "symbol_1"}) +
        #        Text(" "),
        #          rdescript="LaTeX: Insert symbols"),
        # "<index_operator> from <[big_1]> <symbol_1> to [<big_2>] <symbol_2>":
        #     R(Text("\\") + Text("%(index_operator)s ") + Key("underscore") +
        #         Function(symbol_letters, extra={"big_1", "symbol_1"}) +
        #             Key("right, caret") + Function(symbol_letters, extra={"big_2", "symbol_2"}) +
        #             Key("right")),
        # # "from":
        #     Key("underscore"),
        # "to":
        #     Key("right, caret"),
        # "smath":
        #     Key("c-m"),
    }

    extras = [
        alphanumeric.get_alphabet_choice("letter"),
        Choice("big_1", {
            "big": True,
        }),
        Choice("big_2", {
            "big": True,
        }),
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
        Choice(
            "index_operator", {
                "integ": "int",
                "double integ": "iint",
                "triple integ": "iiint",
                "intersection": "cap",
                "union": "cup",
                "(large direct sum | large oh plus)": "bigoplus",
                "product": "prod",
            }),
        Choice("symbol_1", math_vocab.symbol),
        Choice("symbol_2", math_vocab.symbol),
        Choice("symbol_3", math_vocab.symbol),
        Choice("name", {"bill": "william"})
        # Choice("symbol_2", symbol),
    ]

    defaults = {
        "big": False,
        "symbol_3": None,
    }


control.nexus().merger.add_global_rule(Alphabet())
