from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice, Mouse, Mimic, Playback)
from castervoice.lib import context, navigation, alphanumeric, textformat, text_utils
from castervoice.lib import control 
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils


class AlexCcrRule(MergeRule):
    #pronunciation = CCRMerger.CORE[5]
    
    mapping = {
        "sample command": Key("b"), 
         "mick": Mouse("left:1"),
          "dick": Mouse("left:2"),
          "rick": Mouse("right"),
        "Key": R(Text('Key("")') + Key("left:2")),
        "Text": R(Text('Text("")') + Key("left:2")),
        "Mouse": R(Text('Mouse("")') + Key("left:2")),
        "code Pause": R(Text('Pause("")') + Key("left:2")),
        "Mimic": R(Text('Mimic("")') + Key("left:2")),
        "Repeat": Text(" * Repeat(extra='n'),"),
        "Choice": Text('Choice("", {)') + Key("enter:2") + Text("},") + Key("up:2, right:5"),
        "plusser": Text(" + "),
        "eaker": Text(" = "),
        "kohler": Key("right") + Text(": "),
         "smack [<n>] [<my_words>]": R(Key("cs-left:%(n)s, del") + Text("%(my_words)s")),
         "frack [<n>] [<my_words>]": R(Key("cs-right:%(n)s, del") + Text("%(my_words)s")),
         "salor [<n>]": R(Key("cs-left:%(n)s")),
         "jalor [<n>]": R(Key("cs-right:%(n)s")),
         "lor [<n>] [<my_words>]": Key("c-left:%(n)s") + Text("%(my_words)s"),
         "ror [<n>] [<my_words>]": Key("c-right:%(n)s") + Text("%(my_words)s"),
         "ranter": Key("end"),
         "lanter": Key("home"),
        'strike [<n>]': Playback([(["scratch", "that"], 0.03)]) * Repeat(extra="n"),
        
        
        "runnoo [<n>]": Key("c-z") * Repeat(extra="n"), # undo
        "embed gitter": Key("backtick:3, s-enter:2, backtick:3, up"),
        "pounce <dict>": Text("%(dict)s") + Key("enter"),
        

        #  "mimic recognition <text> [<n> times]":
        #             Mimic(extra="text") * Repeat(extra="n"),
     
        


    }

    extras = [
    Dictation("my_words"),
    Dictation("dict"),
    Dictation("text"),

    IntegerRefST("n", 0, 10),        
    ]
    defaults = {
        
        "dictation": "",
        "dict": "",
        "text": "",
        "my_words": "",
        "n": "1",
    }
    
control.nexus().merger.add_global_rule(AlexCcrRule()) 


