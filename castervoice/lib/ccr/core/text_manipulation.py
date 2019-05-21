from dragonfly import Function, Key, Text, Mouse, Pause, Dictation, Choice, Grammar 


from castervoice.lib import control, settings, text_manipulation_functions

from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils
from castervoice.apps import reloader
from castervoice.apps import reloader



class TextManipulation(MergeRule):
    # non = NavigationNon
    # pronunciation = CCRMerger.CORE[4]
    pronunciation = "text manipulation"


    mapping = {
        "bathroom": R(Text("de"), rdescript="red blue"), 
        "Tiger": Key("up:0"),

        
        "(replace|to) <lease_ross> [<number_of_lines_to_search>] <dictation> (with|to) <dictation2>":
            R(Function(text_manipulation_functions.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right")),
              rdescript="Core: replace text to the left or right of the cursor"),
        
        "remove <lease_ross> [<number_of_lines_to_search>] <dictation>":
            R(Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase", lease_ross="left_right")),
              rdescript="remove chosen phrase to the left or right of the cursor"),
        "remove lease [<number_of_lines_to_search>] <left_character>":
            R(Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(left_character="phrase"),
                       left_right="left"),
              rdescript="remove chosen character to the left of the cursor"),
        "remove ross [<number_of_lines_to_search>] <right_character>":
            R(Function(text_manipulation_functions.copypaste_remove_phrase_from_text,
                       dict(right_character="phrase"),
                       left_right="right"),
              rdescript="remove chosen character to the right of the cursor"),

        # problem: sometimes Dragon thinks the before-and-after variable is part of dictation.      
        "go <lease_ross> [<number_of_lines_to_search>] [<before_after>] <dictation>":
            R(Function(text_manipulation_functions.move_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right")),
              rdescript="move to chosen phrase to the left or right of the cursor"),
        "go lease [<before_after>] [<number_of_lines_to_search>] <left_character>":
            R(Function(text_manipulation_functions.move_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left"),
              rdescript="move to chosen character to the left of the cursor"),
        "go ross [<before_after>] [<number_of_lines_to_search>] <right_character>":
            R(Function(text_manipulation_functions.move_until_phrase,
                       dict(right_character="phrase"),
                       left_right="right"),
              rdescript="move to chosen character to the right of the cursor"),
        "grab <lease_ross> [<number_of_lines_to_search>] <dictation> ":
            R(Function(text_manipulation_functions.select_phrase, dict(dictation="phrase", lease_ross="left_right")),
                 rdescript="select chosen phrase"),
        "grab lease [<number_of_lines_to_search>] <left_character>":
            R(Function(text_manipulation_functions.select_phrase, dict(left_character="phrase"), left_right="left"),
            rdescript="select chosen character to the left"),
        "grab ross [<number_of_lines_to_search>] <right_character>":
            R(Function(text_manipulation_functions.select_phrase, dict(right_character="phrase"), left_right="right"),
            rdescript="select chosen character to the right"),
        
        "grab <lease_ross> [<number_of_lines_to_search>] until <dictation> ":
            R(Function(text_manipulation_functions.select_until_phrase, dict(dictation="phrase", lease_ross="left_right")),
                 rdescript="select until chosen phrase (inclusive)"),
        "grab lease [<number_of_lines_to_search>] until <left_character>":
            R(Function(text_manipulation_functions.select_until_phrase, dict(left_character="phrase"), left_right="left"),
            rdescript="select left until chosen character"),
        "grab ross [<number_of_lines_to_search>] until  <right_character>":
            R(Function(text_manipulation_functions.select_until_phrase, dict(right_character="phrase"), left_right="right"),
            rdescript="select right until chosen character"),
        "wipe <lease_ross> [<number_of_lines_to_search>] [<before_after>] <dictation>":
            R(Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(dictation="phrase", lease_ross="left_right")),
              rdescript="delete left until chosen phrase (exclusive)"),
        "wipe lease [<number_of_lines_to_search>] [<before_after>] <left_character>":
            R(Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(left_character="phrase"),
                       left_right="left"),
              rdescript="delete left until chosen character (exclusive)"),
        "wipe ross [<number_of_lines_to_search>] [<before_after>] <right_character>":
            R(Function(text_manipulation_functions.copypaste_delete_until_phrase,
                       dict(right_character="phrase"), 
                       left_right="right"),
              rdescript="delete left until chosen character"),
        




        
        
    }
    extras = [
        Dictation("dict"),
        Dictation("dictation"),
        Dictation("dictation2"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),
        IntegerRefST("number_of_lines_to_search", 1, 50),
        Choice("character_sequence", {
            "comma": ",",
        }),
     Choice(
            "left_character", {
                "[left] prekris": "(",
                "right prekris": ")",
                "[left] brax": "[",
                "right brax": "]",
                "[left] angle": "<",
                "right angle": ">",
                "[left] curly": "{",
                "right curly": "}",
                "quotes": '"',
                "single quote": "'",
                "comma": ",",
                "(dot | period)": ".",
                "questo": "?",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "x-ray": "x",

            }),
        Choice(
            "right_character", {
                "[right] prekris": ")",
                "left prekris": "(",
                "[right] brax": "]",
                "left brax": "[",
                "[right] angle": ">",
                "left angle": "<",
                "[right] curly": "}",
                "left curly": "{",
                "quotes": '"',
                "single quote": "'",
                "comma": ",",
                "(dot | period)": ".",
                "questo": "?",
                "backtick": "`",
                "equals": "=",
                "dolly": "$",
                "slash": "/",
                "backslash": "\\",
                "minus": "-",
                "plus": "+",
                "starling": "*",
                "x-ray": "x",
                
            }),
        Choice("lease_ross", {
            "lease": "left",
            "ross": "right",
        }),
        Choice("before_after", {
            "before": "before",
            "after": "after",
        }),
        
        
    ]
    defaults = {"n": 1, "m": 1, "spec": "", "dict": "", "text": "", "mouse_button": "", 
        "horizontal_distance": 0, "vertical_distance": 0, 
        "lease_ross": "left",
        "before_after": None,
        "number_of_lines_to_search": 0,}

control.nexus().merger.add_global_rule(TextManipulation())



