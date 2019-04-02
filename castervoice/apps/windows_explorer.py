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
        "up [<n>]":
            R(Key("a-up"), rdescript="File Dialogue: Navigate up")*Repeat(extra="n"),
        "back [<n>]":
            R(Key("a-left"), rdescript="File Dialogue: Navigate back")*Repeat(extra="n"),
        "forward [<n>]":
            R(Key("a-right"), rdescript="File Dialogue: Navigate forward")*
            Repeat(extra="n"),
        # "(files | file list)":
        #     R(Key("a-d, f6:3"), rdescript="File Dialogue: Files list"),
        # "navigation [pane]":
        #     R(Key("a-d, f6:2"), rdescript="File Dialogue: Navigation pane"),
        # "[file] name":
        #     R(Key("a-d, f6:5"), rdescript="File Dialogue: File name"),

        "<location>": Key("c-l, tab:%(n)s"),
        "layout": Key("a-v, l") + Mimic("small", "icons"),

    }

    extras = [IntegerRefST("n", 1, 10),
        Choice("location", {
            "search": 1,
            "left pane": 2,
            "center pane": 3,
            "namer": 4,
        }),
    ]
    defaults = {
        "n": 1,
    }


context = AppContext(title="Explorer")

grammar = Grammar("WindowsExplorer", context=context)
if settings.SETTINGS["apps"]["windows_explorer"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FileDialogueRule())
    else:
        rule = FileDialogueRule()
        gfilter.run_on(rule)
        grammar.add_rule(FileDialogueRule(name="filedialogue"))
        grammar.load()
