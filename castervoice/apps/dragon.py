
# from dragonfly import (Grammar, Playback, Key, Dictation, Function, Choice, Mimic, WaitWindow, Pause, Repeat)
from dragonfly import *
from castervoice.lib import control
from castervoice.lib import utilities, settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

_NEXUS = control.nexus()


def fix_dragon_double(nexus):
    try:
        lr = nexus.history[len(nexus.history) - 1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del").execute()
    except Exception:
        utilities.simple_log(False)

def cap_dictation(dictation):
    input_list = str(dictation).split(" ")
    output_list = []
    for i in range(len(input_list)):
        if input_list[i] == "cap":
            input_list[i+1] = input_list[i+1].title()
        else:
            output_list.append(input_list[i])
    Text(" ".join(output_list)).execute()


class DragonRule(MergeRule):
    pronunciation = "dragon"

    mapping = {
        "format <dictation>": Function(cap_dictation, extra={"dictation"}),
        '(lock Dragon | deactivate)':
            R(Playback([(["go", "to", "sleep"], 0.0)]), rdescript="Dragon: Go To Sleep"),
        '(number|numbers) mode':
            R(Playback([(["numbers", "mode", "on"], 0.0)]),
              rdescript="Dragon: Number Mode"),
        'spell mode':
            R(Playback([(["spell", "mode", "on"], 0.0)]), rdescript="Dragon: Spell Mode"),
        'dictation mode':
            R(Playback([(["dictation", "mode", "on"], 0.0)]),
              rdescript="Dragon: Dictation Mode"),
        'normal mode':
            R(Playback([(["normal", "mode", "on"], 0.0)]),
              rdescript="Dragon: Normal Mode"),
        'com on':
            R(Playback([(["command", "mode", "on"], 0.0)]),
              rdescript="Dragon: Command Mode (On)"),
        'com off':
            R(Playback([(["command", "mode", "off"], 0.0)]),
              rdescript="Dragon: Command Mode (Off)"),
        'scratch':
            R(Playback([(["scratch", "that"], 0.0)]), rdescript="Dragon: 'Scratch That'"),
        "reboot dragon":
            R(Function(utilities.reboot), rdescript="Reboot Dragon Naturallyspeaking"),
        "fix dragon double":
            R(Function(fix_dragon_double, nexus=_NEXUS),
              rdescript="Fix Dragon Double Letter"),
        "left point":
            R(Playback([(["MouseGrid"], 0.1), (["four", "four"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Left Point"),
        "right point":
            R(Playback([(["MouseGrid"], 0.1), (["six", "six"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Right Point"),
        "center point":
            R(Playback([(["MouseGrid"], 0.1), (["click"], 0.0)]),
              rdescript="Mouse: Center Point"),

        # new commands from Alex      
        "windows": Mimic("list", "all", "windows"), # this emulates a useful native dragon command
        "cory <dict>": 
            R(Mimic("correxct", extra="dict") + WaitWindow(title="spelling window") + Mimic("choose", "one"),
                rdescript="brings up the correction menu for the phrase spoken in the command and chooses the 1st choice"),
        "cory that": 
            R(Mimic("correct", "that") + WaitWindow(title="spelling window") + Mimic("choose", "one"), 
                rdescript="brings up the correction menu for the previously spoken phrase"),

        "make that <dict>": Mimic("scratch", "that") + Mimic(extra="dict"), 
        'strike [<n>]': Playback([(["scratch", "that"], 0.03)]) * Repeat(extra="n"),
        "train word": Mimic("train", "that") + Key("a-r/200, s"),
        "(trad | add train)": Key("a-a/2, enter/300, a-s"),
        # create an awesome add word command

        "recognition history": 
            Playback([(["view", "recognition", "history"], 0.03)]),
        "peak [recognition] history": 
            Playback([(["view", "recognition", "history"], 0.03)])
                + Pause("200") + Key("escape"),
        "[dictation] sources": Mimic("manage", "dictation", "sources"),
        
        "<dict> (Peru)": Text(''),
        "(talk | talking) <dict>": Text(''),
        "<dict> (Brazil)": Mimic("go", "to", "sleep"),

        # the following commands should be context specific to the Dragon spelling window
        "<first_second_third> word": 
            Key("home, c-right:%(first_second_third)d, cs-right"), 
        "last [word]": Key("right, cs-left"),
        "second last word": Key("right, c-left:1, cs-left"),
        "<number>": Mimic("choose", extra="number"), # instead of having to say e.g. choose one you can just say one
    }
    extras = [
        Dictation("text"),
        Dictation("dict"),
        Dictation("dictation"),
        Dictation("mim"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("number", 1, 10),
        Choice("first_second_third", {
            "first": 0,
            "second": 1,
            "third": 2,
            "fourth": 3,
            "fifth": 4,
            "six": 5,
            "seventh": 6
        }),
        
    ]
    defaults = {"n": 1, "mim": "", "text": "", "dict": "", "dictation": ""}


#---------------------------------------------------------------------------

grammar = Grammar("Dragon Naturallyspeaking")

if settings.SETTINGS["apps"]["dragon"] and not settings.WSR:
    rule = DragonRule(name="dragon")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    grammar.load()
