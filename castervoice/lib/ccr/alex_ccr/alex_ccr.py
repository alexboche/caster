from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat,
                       Function, Choice, Mouse, Mimic, Playback)
from castervoice.lib import context, navigation, alphanumeric, textformat, text_utils
from castervoice.lib import control 
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge.ccrmerger import CCRMerger
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils

from dragonfly.actions.action_mouse import get_cursor_position


def split_dictation(text):
    if text:
        words = ['"%s"' % word for word in text.format().split()]
        words = ', '.join(words)
    else:
        words = '""'

    return words


def type_split_dictation(text):
    Text(split_dictation(text)).execute()


def type_mimic(text):
 
   # Create an argument list for Mimic from text.
    words = split_dictation(text)

    # Define the action to execute. Move back only if no words were
    # specified.
    action = Text('Mimic(%s)' % words)
    if not text:
        action += Key("left:2")

    # Execute the action.
    action.execute()


def type_playback(text):
    # Create an argument list for Playback from text.
    words = split_dictation(text)

    # Define the action to execute.
    # This will press enter a few times. Indentation will depend on your
    # editor.
    enter = Key("enter")
    action = (Text('Playback([') + enter +
              Text('([%s], 0.0),' % words) + enter +
              Text('])') + Key("up, end"))

    # Move back only if no words were specified.
    if not text:
        action += Key("left:9")

    # Execute the action.
    action.execute()


def type_mouse(mouse_button):
    action = Text('Mouse("%s")' % mouse_button)

    # Move back only if no words were specified.
    if not mouse_button:
        action += Key("left:2")

    # Execute the action.
    action.execute()

def type_mouse_current():
    # Type Mouse("[X, Y]"). The typed Mouse action will move the cursor to
    # back to where it was when the command was spoken.
    Text('Mouse("[%d, %d]")' % get_cursor_position()).execute()


class AlexCcrRule(MergeRule):
    #pronunciation = CCRMerger.CORE[5]
    
    mapping = {
        "sample command": Key("b"), 
         "mick": Mouse("left:1"),
          "dick": Mouse("left:2"),
          "rick": Mouse("right"),
        "middle click": Mouse("middle"),
        "say <dict>": Text("%(dict)s"),        
        "center click": Mouse("[0.5, 0.5], left"),


        "hard delete [<n>]": Key("s-delete") * Repeat(extra='n'),
        "lanter": Key("home"),
        "ranter": Key("end"),
         "jack [<n>] [<my_words>]": R(Key("cs-left:%(n)s, del") + Text("%(my_words)s")),
        "smack [<n>]": R(Key("cs-left:%(n)s, del")),
        # "mack [<n>] [<my_words>]": R(Key("cs-right:%(n)s, del") + Text("%(my_words)s")),
        "frack [<n>]": R(Key("cs-right:%(n)s, del")),
        #  "salor [<n>]": R(Key("cs-left:%(n)s")),
        #  "jalor [<n>]": R(Key("cs-right:%(n)s")),
        #  "palor [<n>] [<my_words>]": Key("c-left:%(n)s") + Text("%(my_words)s"),
         "(previous word | lor) [<n>]": Key("c-left:%(n)s"),
        #  "kalor [<n>] [<my_words>]": Key("c-left:%(n)s") + Text("%(my_words)s"),
         "(next word |  ralar) [<n>]": Key("c-right:%(n)s"),
         "back tab [<n>]": Key("s-tab%(n)s"),
        
        "runnoo [<n>]": Key("c-z") * Repeat(extra="n"), # undo
        "embed gitter": Key("backtick:3, s-enter:2, backtick:3, up"),
        "pounce <dict>": Text("%(dict)s") + Key("enter"),
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


