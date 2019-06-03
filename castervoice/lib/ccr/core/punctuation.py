from dragonfly import Choice, Repeat

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

text_punc_dict = {
    "semper":                               ";",
    "[is] greater than":                    ">",  
    "[is] less than":                       "<",
    "[is] greater [than] [or] equal [to]": ">=",
    "[is] less [than] [or] equal [to]":    "<=",
    "[is] equal to":                       "==",
    "equals":                               "=",
    "plus":                                 "+",
    "minus":                                "-",
    "pipe (sim | symbol)":                  "|",
    "ace":                                  " ",
    "clamor":                               "!",     
    "deckle":                               ":",
    "starling":                             "*",  
    "questo":                               "?", 
    "comma":                                ",",  
    "carrot":                               "^", 
    "(period | dot)":                       ".", 
    "(atty | at symbol)":                   "@", 
    "hash tag":                             "#",
    "apostrophe | single quote | chicky":   "'",   
    "underscore":                           "_",
    "backslash":                           "\\", 
    "slash":                                "/",
    "Dolly":                                "$",
    "modulo":                               "%",
    "ampersand":                            "&",
    "tilde":                                "~",
    "(left prekris | lay)":                 "(",
    "(right prekris | ray)":                ")",
    "(left brax | lack)":                   "[",
    "(right brax | rack)":                  "]",
    "(left angle | lang)":                  "<",
    "(right angle | rang)":                 ">",
    "(left curly | lace)":                  "{",
    "(right curly | race)":                 "}",
    "ticky":                                "`",
    "chocky":                              "\"",
}

double_text_punc_dict = {
    "quotes":                            "\"\"",
    "thin quotes":                         "''",
    "bakes":                               "``",
    "prekris":                             "()",
    "brax":                                "[]",
    "curly":                               "{}",
    "angle":                               "<>",
}

class Punctuation(MergeRule):
    pronunciation = CCRMerger.CORE[3]

    mapping = {
        "semper":
            R(Key("semicolon"), rdescript="Semicolon"),
        "quotes":
            R(Key("dquote,dquote,left"), rdescript="Quotation Marks"),
        "thin quotes":
            R(Key("apostrophe,apostrophe,left"), rdescript="Thin Quotation Marks"),
        "[is] greater than":
            R(Key("rangle"), rdescript="> Comparison"),
        "[is] less than":
            R(Key("langle"), rdescript="< Comparison"),
        "[is] greater [than] [or] equal [to]":
            R(Key("rangle, equals"), rdescript=">= Comparison"),
        "[is] less [than] [or] equal [to]":
            R(Key("langle, equals"), rdescript="<= Comparison"),
        "[is] equal to":
            R(Key("equals, equals"), rdescript="Equality"),
        "double": Key("space, equals, equals, space"),
        "prekris":
            R(Key("lparen, rparen, left"), rdescript="Parentheses"),
        "brax":
            R(Key("lbracket, rbracket, left"), rdescript="Square Brackets"),
        "curly":
            R(Key("lbrace, rbrace, left"), rdescript="Curly Braces"),
        "angle":
            R(Key("langle, rangle, left"), rdescript="Angle Brackets"),
        "[<long>] equals":
            R(Text("%(long)s" + "=" + "%(long)s"), rdescript="Equals Sign"),
        "[<long>] plus":
            R(Text("%(long)s" + "+" + "%(long)s"), rdescript="Plus Sign"),
        "[<long>] minus":
            R(Text("%(long)s" + "-" + "%(long)s"), rdescript="Dash"),
        "piper":
            R(Text("|"), rdescript="Pipe Symbol"),
        'ace [<npunc>]':
            R(Key("space"), rdescript="Space")*Repeat(extra="npunc"),
        "clamor":
            R(Text("!"), rdescript="Exclamation Mark"),
        "deckle":
            R(Text(":"), rdescript="Colon"),
        "Faisal": Text(": "),
        "starling":
            R(Key("asterisk"), rdescript="Asterisk"),
        "questo":
            R(Text("?"), rdescript="Question Mark"),
        "comma":
            R(Text(","), rdescript="Comma"),
        "carrot":
            R(Text("^"), rdescript="Carat"),
        "(period | dot)":
            R(Text("."), rdescript="Dot"),
        "atty":
            R(Text("@"), rdescript="At Sign"),
        "hash tag":
            R(Text("#"), rdescript="Hash Tag"),
        "(apostrophe | appy)":
            R(Text("'"), rdescript="Apostrophe"),
        "score":
            R(Text("_"), rdescript="Underscore"),
        "backslash":
            R(Text("\\"), rdescript="Back Slash"),
        "slash":
            R(Text("/"), rdescript="Forward Slash"),
        "Dolly":
            R(Text("$"), rdescript="Dollar Sign"),
        "moddy":
            R(Key("percent"), rdescript="Percent Sign"),
        'tabby [<npunc>]':
            R(Key("tab"), rdescript="Tab")*Repeat(extra="npunc"),
        "boom":
            R(Text(", "), rdescript="Comma + Space"),
        "ampersand":
            R(Key("ampersand"), rdescript="Ampersand"),
        "tilde":
            R(Key("tilde"), rdescript="Tilde"),
        "absolute": R(Text("||") + Key("left")),
        
        
        "lazer": Key("lparen"),
        "razer": Key("rparen"),
        "lapper": Key("lbrace"),
        "rapper": Key("rbrace"),
        "lacky": Key("lbracket"),
        "racky": Key("rbracket"),
        "langle": Key("langle"),
        "rangle": Key("rangle"),
              "stingle": Key("squote"),
        "doter": Key("dquote"),
        "backtick": Key("backtick"),


    }

    extras = [
        IntegerRefST("npunc", 0, 10),
        Choice("long", {
              "long": " ",
        }),

    ]
    defaults = {
        "npunc": 1,
        "long": "",
    }


control.nexus().merger.add_global_rule(Punctuation())
