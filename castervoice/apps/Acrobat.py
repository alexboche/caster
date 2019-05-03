#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Adobe Acrobat

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat, Choice, Mouse, Pause)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R



class AcrobatRule(MergeRule):
    pronunciation = "acrobat"

    mapping = {

        "(close|hide) bookmarks [pane]": R(Key("a-v/15, down:7, right, n, b"),
             rdescript="close bookmarks pane"),
        "pager <n>": R(Key("a-v, n, g/15") + Text("%(n)s") + Key("enter"),
            rdescript="go to page acrobat)"),
        "open": R(Key("c-o")),
        "nindow":R(Key("a-w,n/40,ws-left")),
        "enable scrolling": R(Key("a-v, p, c")),
        "disable scrolling": R(Key("a-v, p, s")),
        "(next tab | nab) [<n>]": R(Key("c-tab")) * Repeat(extra="n"),
        "(previous tab | lab) [<n>]": R(Key("cs-tab")) * Repeat(extra="n"),
        "(home button|homer)": R(Mouse("[100, 101], left")),

        
        # Sticky Note Commands
            # must have the cursor over the location where you want the sticky note
        "add note [<dict>]": R(Mouse("right") + Key("t/5") + Text("%(dict)s"),
             rdescript="add sticky note with dictation"),
        "fast [add] note [<dict>]":
            R(Mouse("right") + Key("t/5") + Text("%(dict)s") + Pause("10") + Key("escape/5, c-s"),
             rdescript="add sticky note with dictation then close it and save"),
        "open blank note":
            R(Mouse("right") + Key("t/5"), rdescript="open sticky note"),
        "add blank note":
            R(Mouse("right") + Key("t/5, escape/5, c-s"),
                rdescript="open sticky note, close it, and then save"),
        "delete note":
            R(Mouse("right") + Key("l, c-s"), rdescript="close sticky note then save"),
      

        
        
        "back": Key("a-left"),
        "save as": R(Key("a-f, a"), rdescript=""),
        "fast save": Key("c-s/10, enter/20, enter/20, left, enter"),
        "down it [<n>]": R(Key("pgdown:%(n)s, up:3"), rdescript=""),
        "up it [<n>]": R(Key("pgup:%(n)s, down:3"), rdescript=""),

        "[navigation] tree": Key("a-v, s, n, e"),
        
        "rotate [<n>]": Key("c-plus") * Repeat(extra='n'),

        # scrolling commands
        "scroll <m>": Key("cs-h/2, %(m)s"),
        "scroll": Key("cs-h/2, 6"),
        "rescroll <m>": Key("%(m)s, %(m)s"),
        "reverse [direction]": Key("minus"), 
        "stop [scrolling]": Key("escape"),

        # cursor commands (must enable "you single key accelerators to access tools" by going to edit>preferences>general)
        "highlight": R(Key("u"), rdescript=""),
        "hand tool": R(Key("h"), rdescript=""),
        "select tool": R(Key("v"), rdescript=""),

    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 1000),
        IntegerRefST("m", 1, 9),
    ]
    defaults = {"n": 1, "dict": "nothing"}


#---------------------------------------------------------------------------

context = AppContext(executable="acrobat")
grammar = Grammar("acrobat", context=context)

if settings.SETTINGS["apps"]["acrobat"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AcrobatRule())
    else:
        rule = AcrobatRule(name="acrobat")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
