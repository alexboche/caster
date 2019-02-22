import toml
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice, Mouse)
from castervoice.lib import context, navigation, alphanumeric, textformat, text_utils
from castervoice.lib import control 
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils
from castervoice.lib.ccr.core import math_vocab

# formatting for latex symbols without curly braces and all Lyx codes
def format_without_braces(vocab_dict):
    lyx_vocab_dict = {k:"\\{} ".format(vocab_dict[k]) for k in vocab_dict}
    return lyx_vocab_dict

# formatting for LaTeX operators with curly braces only
def format_with_braces(vocab_dict):
    
    latex_vocab_dict = {k:"\\{}{{}} ".format(vocab_dict[k]) for k in vocab_dict}    
    return latex_vocab_dict

def cap_symbol_letters(big, symbol):
    if big:
        symbol = symbol.title()
    return symbol
  
# load the toml file
with io.open("C:\NatLink\NatLink\MacroSystem\caster\lib\ccr\core\math_vocab.toml") as f:
        math_vocab = toml.load(f)

# generate math vocabulary for symbols not requiring braces in latex
non_braces_math_vocab = {}
for category in math_vocab["non_braces"]:
    for spec in math_vocab["non_braces"][category]:
        non_braces_math_vocab[spec] = math_vocab["non_braces"][category][spec]

# generate math vocabulary for symbols requiring braces in latex
braces_math_vocab = {}
for category in math_vocab["braces"]:
    for spec in math_vocab["braces"][category]:
        braces_math_vocab[spec] = math_vocab["braces"][category][spec]

# generate full Lyx math vocabulary
full_lyx_math_vocab = non_braces_math_vocab.copy()
for spec in braces_math_vocab:
    full_lyx_math_vocab[spec] = braces_math_vocab[spec]

        "dick": Mouse("left:2"),
        "rick": Mouse("right"),
        

        "[<big>] <letter>":
            R(Function(alphanumeric.letters2, extra={"big", "letter"}),
              rdescript="Spell"),
        # "word number <wn>":
        #     R(Function(alphanumeric.word_numxber, extra="wn"), rdescript="Number As Word"),
        "numb <wnKK>":
            R(Function(alphanumeric.numbers2, extra="wnKK"),
              rspec="number",
              rdescript="Number"),

        # main math command
        "[<big>] <symbol_1>":
            R(utils.PositionalTexter(cap_symbol_letters, extra=["big", "symbol_1"])),
        
        "dollz": R(Text("$$") + Key("left")),
        "doubledill":R(Text("$$$$") + Key("left:2")),
        "toter": R(Key("right, caret")),
        "<fraction_type> that": R(Key("c-x") + Text("%(fraction_type)s"))
            + Key("c-v, down"),
        "inverse": R(Text("^-1") + Key("right")),
        "squared": R(Text("^2") + Key("right")),
        "cubed": R(Text("^3") + Key("right")),
        "<mathbb_symbol>": R(Text("\mathbb %(mathbb_symbol)s") + Key("right")),
        
        "<accent> [<big>] <symbol_1>": R(Text("%(accent)s") + 
            utils.PositionalTexter(cap_symbol_letters, extra=["big", "symbol_1"]) +
            Key("right")),
        "<accent> [<big>] <letter>": R(Text("%(accent)s") + 
            Function(alphanumeric.letters2, extra={"big", "letter"}) +
            Key("right")),
        "add line": R(Key("c-enter")),
    
        # commented out because I was getting the Natlink error or overly complex grammar.
        # "<index_operator> from <symbol_1> [<symbol_2>] to <symbol_3> [<symbol_4>]":
        #     R(Text("%(index_operator)s_") + Text("%(symbol_1)s") + Text("%(symbol_2)s") + 
        #         Key("right, caret") + Text("%(symbols_3)s") + Text("%(symbols_4)s") +
        #             Key("right")),
        
        # Lyx commands
        "smath":
             Key("c-m"),
        # Lyx insert_menu commands
        "insert <environment>": R(Key("a-i,h") + Text("%(environment)s")),
        "number that": R(Key("a-m, n")),
        "<mode> <my_words>": R(Key("a-p, %(mode)s") + Text("%(my_words)s")),
        "numbered <mode> <my_words>": R(Key("a-p, s-asterisk, %(mode)s") + Text("%(my_words)s")),
        "matrix <m> by <n>": R(Key("a-x") + Text("math-matrix %(m)s %(n)s")) + Key("enter"),
        "delim <delimiter>": R(Key("a-x") + Text("math-delim %(delimiter)s") + Key("enter")),
        

    }

    extras = [
        alphanumeric.get_alphabet_choice("letter"),
        Dictation("my_words"),
        Choice("big", {
            "big": True,
        }),
        Choice("big_2", {
            "big": True,
        }),
        IntegerRefST("m", 0, 10),
        IntegerRefST("n", 0, 10),
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
        Choice(
            "index_operator", 
                format_without_braces(math_vocab["braces"]["index_operators"])),
        Choice(
            "fraction_type", format_without_braces(math_vocab["braces"]["fractions"])),
        Choice(
            "accent", format_without_braces(math_vocab["braces"]["accents"])),
        Choice("delimiter", {"paren": "(", "bracket": "[]"}),

        Choice(
            "mathbb_symbol", {
             "reals": "R",
             "complex": "C",
             "integers": "Z",
             "rationals": "Q",
             "naturals": "N",
            }),    

        Choice("symbol_1", format_without_braces(full_lyx_math_vocab)),
        
        Choice("environment", {
            "(in line formula | in line)": "i",
            "(numbered formula | numbered)": "n",
            "(display formula | display)": "d",
            "equation array": "e",
            "(AMS align environment | AMS align)": "a",
            "AMS align at": "t",
            "AMS flalign": "f",
            "AMS gathered": "g",
            "AMS multline": "m",
            "array ": "y",
            "(cases | piecewise)": "c",
            "aligned": "l",
            "aligned at": "v",
            "gathered": "h",
            "split": "s",
            "delimiters": "r",
            "matrix": "x",
            "macro": "o",
            }),  
        Choice("mode", {
            "standard": "s",
            "(itemize | bullets)": "b",
            "(enumerate | numbering)": "e",
            "description": "d",
            
            "part": "0",
            "section": "2",
            "subsection": "3",
            "subsubsection": "4",
            "paragraph": "5",
            "subparagraph": "6",
            "title": "t",
            "author": "s-a",
            "date": "s-d",
            "abstract": "a",
            "address": "a-a",
            "(bibliography | biblio)": "s-b",
            "quotation": "a-q",
            # i'm not sure what the differences between quotation and quote
            "quote": "q",
            "verse": "v",            
        })
    ]

    defaults = {
        "big": False,
        "symbol_1": "",
        "my_words": ""
        # "symbol_2": "",
        # "symbol_3": "",
        # "symbol_4": "",
        # "symbol_5": "",
        # "symbol_6": "",
        # "symbol_7": "",
        # "symbol_8": "",
        # "symbol_9": "",
                
    }


control.nexus().merger.add_global_rule(Alphabet())
