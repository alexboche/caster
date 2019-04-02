
#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""


"""
#---------------------------------------------------------------------------
# from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat, Choice, Function, ActionBase, ActionError, Playback, Mimic, Pause, WaitWindow)
# eyeX mouse stuff
#!python
# -*- coding: utf-8 -*-
from dragonfly import (Grammar, MappingRule)
from dragonfly.actions.action_mouse import get_cursor_position

import subprocess
import pyperclip



eyemouse_handle = None

def create_hidden_window(arguments):
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = subprocess.SW_HIDE
    return subprocess.Popen(
        arguments,
        close_fds=True,
        startupinfo=si,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)


def eyemouse_launcher(kill=False):
    global eyemouse_handle
    if kill:
        if eyemouse_handle:
            eyemouse_handle.terminate()
            eyemouse_handle = None
        else:
            create_hidden_window(["taskkill", "/im", "C:\Users\alex\Desktop\EyeXMouse\compiled\x64\EyeXMouse.exe", "/f"])
    elif not eyemouse_handle:
        eyemouse_handle = create_hidden_window(
            r"C:\Users\alex\Desktop\EyeXMouse\compiled\x64\EyeXMouse.exe")


def move_mouse(left_right, horizontal_distance, up_down, vertical_distance):
    # todo: make some of the arguments optional
    new_mouse_position = list(get_cursor_position())
    # horizontal axis
    if left_right == "left":
        new_mouse_position[0] -=  (horizontal_distance)
    if left_right == "right":
        new_mouse_position[0] += (horizontal_distance)
    # vertical axis: it seems to be inverted
    if up_down == "down":
        new_mouse_position[1] += vertical_distance
    if up_down == "up":
        new_mouse_position[1] -= vertical_distance
    new_mouse_position = tuple(new_mouse_position)
    Mouse("[%d, %d]" % new_mouse_position).execute()



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
        

        # eye X mouse
        "Eye Mouse":
            Function(eyemouse_launcher, kill=False),
        "stop mouse":
            Function(eyemouse_launcher, kill=True),

        # discrete mouse-movement command
        "cursor [<left_right>] [<horizontal_distance>] [<up_down>] [<vertical_distance>]":
            R(Function(move_mouse,
                extra={"left_right", "horizontal_distance", "up_down", "vertical_distance"})),
        
        

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
        "micky": Mouse("[0.5, .87], left:40") + Mouse("[0.29, 0.87]") + Pause("25") + Mouse("left"),
        "ricky": Mouse("[0.5, .87], left:40") + Mouse("[0.32, 0.87]") + Pause("25") + Mouse("left"),
        "cursy": Mouse("[0.5, .87], left:40") + Mouse("[0.37, 0.87]") + Pause("25") + Mouse("left"),
        "cursor":  Mouse("[0.37, 0.87], left"),
        "lefty":  Mouse("[0.29, 0.87], left"),
        "lerfy":  Mouse("[0.29, 0.1], left"),
        
        "righty":  Mouse("[0.32, 0.87], left"),
        "hideout":  Mouse("[0.78, 0.87], left"),
        "bring down":  Mouse("[0.23, 0.1], left"),
        "bring up":  Mouse("[0.23, 0.87], left"),
        

        # terminal
        "caster one": Text("cd C:\Users\\alex\Desktop\caster-1") + Key("enter"),


        # git
        "git add": R(Text("git add "), rdescript=""),
        "git commit": R(Text('git commit -m ""') + Key("left"), rdescript=""),
        "git push": R(Text("git push "), rdescript=""),
        "git clone": R(Text("git clone "), rdescript=""),
        "git checkout": R(Text("git checkout "), rdescript=""),
        "git check out": R(Text("git fetch "), rdescript=""),
        "git branch": R(Text("git branch "), rdescript=""),
        "git status": R(Text("git status ") + Key("enter"), rdescript=""),
        "git diff": R(Text("git diff ") + Key("enter"), rdescript=""),
        "git remote": R(Text("git remote ") + Key("enter"), rdescript=""),
        "git push set upstream orgin": Text("git push --set-upstream origin "),
        "git graph": Text("git log --oneline --all --graph "),
        "git fetch": R(Text("git fetch ")),        




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
            
        # "<application>": BringApp("%(application)s"),
        
            
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

            "chrome": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "coding": r"C:\Users\alex\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "(outlook | mail)": r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
            "powershell": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        }),
         Choice("left_right", {
            "left": "left",
            "right": "right",
        }),
        Choice("up_down", {
            "up": "up",
            "down": "down",
        }),
        IntegerRefST("horizontal_distance", 0, 500),
        IntegerRefST("vertical_distance", 0, 500),
    ]
    defaults = {"n": 1, "m": 1, "spec": "", "dict": "", "text": "", "mouse_button": "", "left_right": "left", 
        "up_down": "up", "horizontal_distance": 0, "vertical_distance": 0}

        

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
