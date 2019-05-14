from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice, Mouse, Mimic, Playback)                       
from dragonfly.actions.action_mouse import get_cursor_position

from castervoice.lib import context, navigation, alphanumeric, textformat, text_utils
from castervoice.lib import control 
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils


_NEXUS = control.nexus()
    


class AlexCcrRule(MergeRule):
    #pronunciation = CCRMerger.CORE[5]
    
    mapping = {
        "Alex hello": Function(navigation.paper),
        "sample command": Key("b"), 
         "mick": Mouse("left:1"),
          "dick": Mouse("left:2"),
          "rick": Mouse("right"),
        "middle click": Mouse("middle"),
        "salor <dict>": Text("%(dict)s"),        
        "center": Mouse("[0.5, 0.5], left"),
        
        # "squat":
        #     R(Function(navigation.left_down, nexus=_NEXUS), rdescript="Mouse: Left Down"),
        # "bench":
        #     R(Function(navigation.left_up, nexus=_NEXUS), rdescript="Mouse: Left Up"),
        # "taller": Key("a-tab"),
        "Roper": Key("end, enter"),
        "hard delete [<n>]": Key("s-delete") * Repeat(extra='n'),
        "rocking": Key("right, comma, enter"),
        "rocker": Key("right, comma, enter, dquote:2, left"),
        # "ecker": Key("escape"),
        "arky":Key("a-tab"),

        "lanter [<n>]": Key("home:%(n)s"),
        "ranter [<n>]": Key("end:%(n)s"),
        # "fly lanter": Key("c-home"),
        # "queue lanter": Key("cs-home"),
        # "shin lanter": Key("s-home"),
        # "fly ranter": Key("c-end"),
        # "queue ranter": Key("cs-end"),
        # "shin ranter": Key("s-end"),
        "win search": Mouse("[80, 60], left"),
        "quick bar": Key("c-l"),
         
        "smack [<n>]": R(Key("cs-left:%(n)s, del")),
                # "frack [<n>]": R(Key("cs-right:%(n)s, del")),
        "sprat [<n>]": R(Key("cs-right:%(n)s, del")),
        #  "salor [<n>]": R(Key("cs-left:%(n)s")),
        #  "jalor [<n>]": R(Key("cs-right:%(n)s")),
        # "palor [<n>] [<my_words>]": Key("c-left:%(n)s") + Text("%(my_words)s"),
        "lor [<n>]": Key("c-left:%(n)s"),
        # "kalor [<n>] [<my_words>]": Key("c-right:%(n)s") + Text("%(my_words)s"),
        "ralar [<n>]": Key("c-right:%(n)s"),
        "back tab [<n>]": R(Key("s-tab"), rdescript="") * Repeat(extra='n'),
        "caps lock": Mimic("press", "caps", "lock"),

        #"trying": Key("cs-p") + Text("insert snippet") + Key("enter") + Text("try/") + Key("enter"),
        "trying": Key("cs-p") + Text("insert snippet") + Key("enter/10") + Text("try/")
            + Key("enter"),




        "undo [<n>]": Key("c-z") * Repeat(extra="n"), # undo
        "embed gitter": Key("backtick:3, s-enter:2, backtick:3, up"),
        # "close time <dict>": Text("%(dict)s") + Key("enter"),
        "cut all": Key("c-a, c-x"),

# don't seem to be working perfectly
        "select down <n_off_one>": Key("s-down:%(n_off_one)s, s-end"),         
        "select up <n_off_one>": Key("s-end, s-up:%(n_off_one)s, s-end"),          
        "copper down <n_off_one>": Key("s-down:%(n_off_one)s, s-end, c-c"),    
        "copper up <n_off_one>": Key("s-end, s-up:%(n_off_one)s, s-end, c-c"),    
        "cutter down <n_off_one>": Key("s-down:%(n_off_one)s, s-end, c-x"),
        "cutter up <n_off_one>": Key("s-end, s-up:%(n_off_one)s, s-end, c-x"),
        "deleter up <n_off_one>": Key("s-end, s-up:%(n_off_one)s, s-end, del"),
        "deleter down <n_off_one>": Key("s-down:%(n_off_one)s, s-end, del"),
    
    
    
        


    }
    

    extras = [
    Dictation("my_words"),
    Dictation("dict"),
    Dictation("text"),
    Choice("mouse_button", {
            "left": "left",
            "right": "right",
            "middle": "middle",
    }),
    
    IntegerRefST("n", 0, 10),       
    Choice("n_off_one", {
        "one": 0,
        "two": 1,
        "three": 2,
        "four": 3,
        "five": 4,
        "six": 5,
        "seven": 6,
        "eight": 7,
        "nine": 8,
        "ten": 9,
        "eleven": 10,
        "twelve": 11,
        "thirteen": 12,
        "fourteen": 13,
        "fifteen": 14,
        "sixteen": 15,
        "seventeen": 16,
        "eighteen": 17,
        "nineteen": 18,
        "twenty": 19,
        

        }),
    
    ]
    defaults = {
        
        "dictation": "",
        "dict": "",
        "text": "",
        "my_words": "",
        "n": "1",
        "mouse_button": "",
    }
    
control.nexus().merger.add_global_rule(AlexCcrRule()) 


