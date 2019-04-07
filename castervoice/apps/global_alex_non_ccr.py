# import _RemapArgsFunction
# from dragonfly.actions.action_function import RemapArgsFunction

from inspect           import getargspec
# from action_base      import ActionBase, ActionError
from dragonfly.actions.action_base import ActionBase, ActionError




class RemapArgsFunction(ActionBase):
    # def __init__(self, function, remap_data=None, **defaults):
    def __init__(self, function, defaults=None, remap_data=None):
    
        ActionBase.__init__(self)
        self._function = function
        self._defaults = defaults or {}
        self._remap_data = remap_data or {}
        self._str = function.__name__

        # TODO Use inspect.signature instead; getargspec is deprecated.
        (args, varargs, varkw, defaults) = getargspec(self._function)
        if varkw:  self._filter_keywords = False
        else:      self._filter_keywords = True
        self._valid_keywords = set(args)

    def _execute(self, data=None):
        arguments = dict(self._defaults)
        if isinstance(data, dict):
            arguments.update(data)

        # Remap specified names.
        if arguments and self._remap_data:
            for old_name, new_name in self._remap_data.items():
                if old_name in data:
                    arguments[new_name] = arguments.pop(old_name)

        if self._filter_keywords:
            invalid_keywords = set(arguments.keys()) - self._valid_keywords
            for key in invalid_keywords:
                del arguments[key]

        try:
            self._function(**arguments)
        except Exception as e:
            self._log.exception("Exception from function %s:"
                                % self._function.__name__)
            raise ActionError("%s: %s" % (self, e))
#---------------------------------------------------------------------------



#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""


"""
#-------------------------------
# from dragonfly import (Grammar, AppContext, Dictation, Key, Text, Repeat, Choice, Function, ActionBase, ActionError, Playback, Mimic, Pause, WaitWindow)
# eyeX mouse stuff
#!python
# -*- coding: utf-8 -*-
# from dragonfly import (Grammar, MappingRule, Function)
# from dragonfly import *
from dragonfly.actions.action_mouse import get_cursor_position

import subprocess
import pyperclip
import io
# from castervoice.alex_text_manipulation.copypaste import package/module


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




def cap_dictation(dictation):
    input_list = str(dictation).split(" ")
    output_list = []
    for i in range(len(input_list)):
        if input_list[i] == "cap":
            input_list[i+1] = input_list[i+1].title()
        else:
            output_list.append(input_list[i])
    Text(" ".join(output_list)).execute()


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

# storage file
file_name = r"C:\NatLink\NatLink\MacroSystem\castervoice\alex_text_manipulation\storage.txt"
    

def save_clipboard_to_file():
    s = pyperclip.paste()
    file_name = r"C:\NatLink\NatLink\MacroSystem\castervoice\alex_text_manipulation\storage.txt"
    with io.open(file_name, 'w') as f:
        f.write(s)

def delete_current_sentence(left_string, right_string):
    # cursor_position  = len(left_string)
    previous_period_location = left_string.rfind(".")
    next_period_location = right_string.find(".")

    # new_left_string includes the period
    new_left_string = left_string[:previous_period_location + 1]

    # new_right_string includes the space after the period.
    new_right_string = right_string[next_period_location + 1:]

    # full_string = new_left_string + new_right_string

    return (new_left_string, new_right_string)

def deleter():
    file_name = r"C:\NatLink\NatLink\MacroSystem\castervoice\alex_text_manipulation\storage.txt"
    left_string = ""
    with io.open(file_name, 'r') as f:
        left_string = f.read()
    right_string = pyperclip.paste()
    new_left_string, new_right_string = delete_current_sentence(left_string, right_string)
    # new_right_string = delete_current_sentence(left_string, right_string)[1]
    pyperclip.copy(new_right_string)
    Key("c-a/2, c-v/2, cs-home/2, left/2").execute() 
    pyperclip.copy(new_left_string)
    Key("c-v/2").execute()



def move_until_character_sequence(left_right, character_sequence):
    if left_right == "left":
        Key("s-home, c-c/2").execute()
        Key("right").execute()
    if left_right == "right":
        Key("s-end, c-c/2").execute()
        Key("left").execute()

    character_sequence = str(character_sequence).lower()
    text = pyperclip.paste()    
    # don't distinguish between upper and lowercase
    text = text.lower()
    if left_right == "left":
        if text.rfind(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.rfind(character_sequence) + len(character_sequence)
            offset = len(text) - character_sequence_start_position 
            Key("left:%d" %offset).execute()
    if left_right == "right":
        if text.find(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.find(character_sequence) 
            offset = character_sequence_start_position 
            Key("right:%d" %offset).execute()
        


def copypaste_delete_until_character_sequence(left_right, character_sequence):
        if left_right == "left":
            Key("s-home, c-c/2").execute()
        if left_right == "right":
            Key("s-end, c-c/2").execute()
        character_sequence = str(character_sequence).lower()
        text = pyperclip.paste()
        # don't distinguish between upper and lowercase
        text = text.lower()
        new_text = delete_until_character_sequence(text, character_sequence, left_right)
        offset = len(new_text)
        pyperclip.copy(new_text)
        Key("c-v/2").execute()
        # move cursor back into the right spot. only necessary for left_right = "right"
        if left_right == "right":
            Key("left:%d" %offset).execute()
        

def delete_until_character_sequence(text, character_sequence, left_right):
    if left_right == "left":
        if text.rfind(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.rfind(character_sequence)
            new_text_start_position = character_sequence_start_position 
            new_text = text[:new_text_start_position]
            return new_text
    if left_right == "right":
        if text.find(character_sequence) == -1:
            raise IndexError("character_sequence not found")
        else:
            character_sequence_start_position = text.find(character_sequence)
            new_text_start_position = character_sequence_start_position + len(character_sequence)
            new_text = text[new_text_start_position:]
            return new_text

        

def add(x, y, z, w):
    sum = x+y+z+w
    print(sum)


# Function.remap(y='q').build(f, x=1)
# Function(f, x=1).remap(y='q')

# Function(f, remap_data=dict(a='d'), defaults=dict(x=1))
# Function.simple(f, x=1)

storeLeftString = Key("cs-home, c-c/2") + Function(save_clipboard_to_file)
class GlobalAlexNonCcrRule(MergeRule):
    pronunciation = "global alex rule"


    mapping = {
        "red blue": R(Text("gr"), rdescript="red blue"), 
        # "add <n> <m> plus five plus six": RemapArgsFunction(add, dict(n='x', m='y'),  z=5, w=6),
        "add <n> <m>": Function(lambda n,m: add(n, m, 5, 6)),
        # "add <ints>": _otherfunction.OtherFunction(add, dict(z=5, w=6), dict(ints='x', n='y')),

        #"delete current sentence": storeLeftString + Key("cs-end, c-c/2, c-a") + Function(deleter) + Key("c-v"),
        "delete current sentence": storeLeftString + Key("cs-end, c-c/2, c-a") + Function(deleter),
        # "delete <left_right> <character_sequence>": 
        #     Function(copypaste_delete_until_character_sequence, extra={"left_right", "character_sequence"}),
        #     Function(copypaste_delete_until_character_sequence, left_right="left"),
        "leeser <left_character>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "left"), dict(left_character="character_sequence")),
        "rosser <right_character>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "right"), dict(right_character="character_sequence")),
        "leeser <dictation>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "left"), dict(dictation="character_sequence")),
        "rosser <dictation>": RemapArgsFunction(move_until_character_sequence, dict(left_right = "right"), dict(dictation="character_sequence")),


        "reload grammars": R(Function(reloader.reload_app_grammars)), 
        "save reload": R(Key("c-s") + Function(reloader.reload_app_grammars)),
        "(satch | sosh) [<n>]": Key("alt:down, tab/20:%(n)d, alt:up"),
        

        # eye X mouse
        "Eye Mouse":
            Function(eyemouse_launcher, kill=False),
        "stop mouse":
            Function(eyemouse_launcher, kill=True),

        # discrete mouse-movement command
        # "cursor [<left_right>] [<horizontal_distance>] [<up_down>] [<vertical_distance>]":
        #     R(Function(move_mouse,
        #         extra={"left_right", "horizontal_distance", "up_down", "vertical_distance"})),
        
        

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
        Dictation("dictation"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),
        Choice("character_sequence", {
            "comma": ",",
        }),
        Choice("left_character", {
            "prekris": "(",
            "brax": "[",
            "angle": "<",
            "curly": "{",
            "quotes": '"',
            "single quote": "'",
            "comma": ",",
            "period": ".",
            "questo": "?",
            "backtick": "`",
        }),
        Choice("right_character", {
            "prekris": ")",
            "brax": "]",
            "angle": ">",
            "curly": "}",
            "quotes": '"',
            "single quote": "'",
            "comma": ",",
            "period": ".",
            "questo": "?",
            "backtick": "`",
        }),
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
        Choice("ints", {
            "one": "1",
            "two": "2",
            "three": "3",
        }),
        IntegerRefST("horizontal_distance", 0, 500),
        IntegerRefST("vertical_distance", 0, 500),
    ]
    defaults = {"n": 1, "m": 1, "spec": "", "dict": "", "text": "", "mouse_button": "", 
        "horizontal_distance": 0, "vertical_distance": 0}

        

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
