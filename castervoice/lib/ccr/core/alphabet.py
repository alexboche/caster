import toml
import io
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice, Mouse)
from castervoice.lib import context, navigation, alphanumeric, textformat  
from castervoice.lib import control 
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils


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
        IntegerRefST("number", 2, 100),
        IntegerRefST("wn", 0, 10),
        IntegerRefST("wnKK", 0, 1000000),
        Choice("denominator", {
                "halves": "2",
                "thirds": "3",
                "fourths": "4",
                "fifths": "5",
                "sixths": "6",
                "sevenths": "7",
                "eighths": "8",
                "ninths": "9",
                "tenths": "10",
                "elevenths": "11",
                "twelfths": "12",
                "thirteenths": "13",
                "fourteenths": "14",
                "fifteenths": "15",
                "sixteenths": "16",
                "seventeens": "17",
                "eighteenths": "18",
                "nineteenths": "19",
                "twentieths": "20",
            }),
        Choice("denominator_single", {
                "half": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
                "seventh": "7",
                "eighth": "8",
                "ninth": "9",
                "tenth": "10",
                "eleventh": "11",
                "twelfth": "12",
                "thirteenth": "13",
                "fourteenth": "14",
                "fifteenth": "15",
                "sixteenth": "16",
                "seventeen": "17",
                "eighteenth": "18",
                "nineteenth": "19",
                "twentieth": "20",
            }),

      
    ]

    defaults = {
        "big": False,
        "symbol_1": "",
        "my_words": "",
        "dictation": "",
        "my_words": "",
        "n": "1",
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
