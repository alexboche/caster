
#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""


"""
#---------------------------------------------------------------------------
# from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat, Choice, Function, ActionBase, ActionError, Playback, Mimic, Pause, WaitWindow)
from dragonfly import *

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils
from castervoice.apps import reloader
from castervoice.apps import reloader

def cap_dictation(dictation):
    input_list = str(dictation).split(" ")
    output_list = []
    for i in range(len(input_list)):
        if input_list[i] == "cap":
            input_list[i+1] = input_list[i+1].title()
        else:
            output_list.append(input_list[i])
    Text(" ".join(output_list)).execute()


class GlobalAlexNonCcrRule(MergeRule):
    pronunciation = "global alex rule"




    mapping = {
        "red blue": R(Text("orange"), rdescript="red blue"),
        "reload grammars": R(Function(reloader.reload_app_grammars)), 
        "save reload": R(Key("c-s") + Function(reloader.reload_app_grammars)),
        "(satch | sosh) [<n>]": Key("alt:down, tab/20:%(n)d, alt:up"),
        
        # "(say | sailing) <dictation>": Function(cap_dictation, extra={"dictation"}),        
            # why is the above command not working and breaking this whole file?
        "smart nav": Key("cs-f9"),
        "shesk": Key("w-d"),
        "eck": Key("escape"), 
        #"swap": Key("win:down, f9, win:up"),
        "snarles": Text("hAtdickbootstorew8ght973"),
        "close": Key("a-f4"),
        "task manager": Key("cs-escape"),
        "find [<dict>]": Key("c-f") + Text("%(dict)s"),
        "(display | change display)": Key("w-d/10") + Mouse("[0.9, 0.5], right") + Key("up:2, enter/30, tab:2"),
        "troppy": Key("tab, a-down"), # this tas to and then drops down a drop-down list
        "drop list": Key("a-down"), # drops down a drop-down list
        
        # windows eye control commands (with the control bar on the bottom rather than the top)
        "micky": Mouse("[0.5, .87], left:40") + Mouse("[0.29, 0.87], left"),
        "ricky": Mouse("[0.5, .87], left:40") + Mouse("[0.32, 0.87], left"),
        "cursy": Mouse("[0.5, .87], left:40") + Mouse("[0.37, 0.87], left"),
        "cursor":  Mouse("[0.37, 0.87], left"),
        "lefty":  Mouse("[0.29, 0.87], left"),
        "righty":  Mouse("[0.32, 0.87], left"),
        "hideout":  Mouse("[0.78, 0.87], left"),
        "bring down":  Mouse("[0.23, 0.1], left"),
        "bring up":  Mouse("[0.23, 0.87], left"),

        "vocab": Playback([(["start", "vocabulary", "editor"], 0.03)]) * Repeat(extra="n"),
        "mimic recognition <dict> [<n> times]":
                    Mimic(extra="dict") * Repeat(extra="n"),
        "bocker": Mimic("dictation", "box"),
        "clicker <m> [<wait_time>]": Mouse("left/%(wait_time)s") * Repeat(extra="m"),
        "next groupy [<n>]": Key("w-backtick") * Repeat(extra='n'), # for groupy

        "save": Key("c-s"),
        "open": Key("c-o"),
        "print": Key("c-p"),
        "max": Key("a-space/15, x"),
        "save and refresh [debug file]":  
            Mimic("save") + Pause("20") + Mimic("refresh", "debug", "file"),
        

        "chrome": BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    
        "coding": BringApp(r"C:\Users\alex\AppData\Local\Programs\Microsoft VS Code\Code.exe"),
        "(outlook | mail)": BringApp(r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"),
        "ackro": BringApp(r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
            
        # "<application>": BringApp(r"%(application)s"),
        
            
        "Google <dict>": BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") 
            + Key("c-t/30") + Text("%(dict)s") + Key("enter"),
        "google search <dict>": BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") 
        + Key("c-l") + Text("%(dict)s") + Key("enter"),
        #"spell search": BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") 
        #   + Pause("20") + Key("c-l"),
        "Duck duck <dict>": BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") 
            + Key("c-t/30") + Text("duckduckgo.com") + Key("tab") + Text("%(dict)s") + Key("enter:200, down, enter"),
        "search <search_engine> <dict>": BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") 
            + Key("c-t/30") + Text("%(search_engine)s") + Key("tab") + Text("%(dict)s") + Key("enter"),

  

        
        
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),
        Choice("search_engine", {
            "(wikipedia | wiki)": "wikipedia.org",
            "amazon": "Amazon.com",
            "bing": "bing.com",
            "duck duck go": "duckduckgo.com",
            }),
        Choice("application", {

            "chrome": "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "coding": "C:\Users\alex\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "(outlook | mail)": "C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
        })
        
    ]

    defaults = {"n": 1, "m": 1, "dict": "nothing"}

#---------------------------------------------------------------------------




context = utils.MultiAppContext(relevant_apps={})
grammar = Grammar("global_alex_non_ccr", context=context)

if settings.SETTINGS["apps"]["global_alex_non_ccr"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(GlobalAlexNonCcrRule())
    else:
        rule = GlobalAlexNonCcrRule(name="global_alex_non_ccr")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
