from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule,
                       Pause, Repeat, Text, Choice)
from dragonfly.actions.action_mimic import Mimic

from castervoice.lib import control, settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class FileDialogueRule(MergeRule):
    pronunciation = "file dialogue"

    mapping = {
        "[go] up [<n>]":
            R(Key("a-up"), rdescript="File Dialogue: Navigate up")*Repeat(extra="n"),
        "[go] back [<n>]":
            R(Key("a-left"), rdescript="File Dialogue: Navigate back")*Repeat(extra="n"),
        "forward [<n>]":
            R(Key("a-right"), rdescript="File Dialogue: Navigate forward")*
            Repeat(extra="n"),
        
        "<location>": Key("c-l/10, tab:%(location)s"),
        
        "purple": Text("Alex"),
    }

    extras = [IntegerRefST("n", 1, 10),
        Choice("location", {
            
            "search": 1,
            "organize": 2,
            "left pane": 3,
            "center pane": 4,
            "sort [headings]": 5,
            "file name": 6,
            "file type": 7,
        }),
    ]
    defaults = {
        "n": 1,
    }

# this is the simplest way to set the context in Windows Explorer child Windows (also known as file dialogbox)
context = AppContext(title="open")

grammar = Grammar("WindowsExplorer", context=context)
if settings.SETTINGS["apps"]["windows_explorer"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FileDialogueRule())
    else:
        rule = FileDialogueRule()
        gfilter.run_on(rule)
        grammar.add_rule(FileDialogueRule(name="filedialogue"))
        grammar.load()
