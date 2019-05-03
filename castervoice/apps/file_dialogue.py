from dragonfly import (AppContext, Dictation, Grammar, IntegerRef, Key, MappingRule,
                       Pause, Repeat, Text, Choice, Function)



from castervoice.lib import control, context, utilities, settings
from castervoice.lib.context import paste_string_without_altering_clipboard
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


# note that the tab structure of Windows Explorer window is slightly different than 
# that of Windows Explorer dialogbox (aka child window)
# this file is only for Windows Explorer dialogbox.


CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_PATH"])
if not CONFIG:
    CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
if not CONFIG:
    # logger.warn("Could not load bringme defaults")
    print("Could not load bringme defaults")
    

def dialogue_bring_it(folder_path):
    Key("c-l/5").execute()
    Text("{}".format(folder_path)).execute()
    # Alternate method: is faster but somewhat inconsistent.
        # if not paste_string_without_altering_clipboard(folder_path):
        #     print("failed to paste {}".format(folder_path))
        # Pause("10").execute()
    # Second alternate method:is fast and consistent, but alters the clipboard
        # pyperclip.copy(folder_path)
        # Pause("5").execute()
        # Key("c-v/30").execute()
    Key("enter/20, a-d/5, tab:4").execute() 

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
        "(files | file list)":
            R(Key("a-d, f6:3"), rdescript="File Dialogue: Files list"),
        "navigation [pane]":
            R(Key("a-d, f6:2"), rdescript="File Dialogue: Navigation pane"),
        "[file] name":
            R(Key("a-d, f6:5"), rdescript="File Dialogue: File name"),



        "search [<text>]": R(Key("c-l, tab"), rdescript="File Dialogue: Search"),
        "organize": R(Key("c-l, tab:2"), rdescript="File Dialogue: press 'organize' button"),
        "(left | navigation) pane": R(Key("c-l, tab:3"), rdescript="File dialogue: navigation pane"),
        "(center|file|folder) (list | pane)": R(Key("c-l, tab:4"), rdescript="File Dialogue: file list"),
        "sort [headings]": R(Key("c-l, tab:5"), rdescript="File Dialogue: sort"),
        "filename": R(Key("c-l, tab:6"), rdescript="File Dialogue: filename"),
        "file type": R(Key("c-l, tab:7"), rdescript="File Dialogue: file type"),


        # "<location>": Key("c-l, tab:%(n)d"),
        #"layout": Key("a-v, l") + Mimic("small", "icons"),
        "[(child | dialogue)] bring me <folder_path>":
                R(Function(dialogue_bring_it),
                rdescript="go to preconfigured folder within currently open Windows Explorer child window"),

    }

    extras = [IntegerRefST("n", 1, 10),
        Dictation("text"),
        Choice("folder_path", CONFIG["folder"]),
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


dialogue_names = [
    "open",
    "select",
]

context = AppContext(title="save")
for name in dialogue_names:
    context = context | AppContext(title=name)

grammar = Grammar("FileDialogue", context=context)
if settings.SETTINGS["apps"]["filedialogue"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(FileDialogueRule())
    else:
        rule = FileDialogueRule()
        gfilter.run_on(rule)
        grammar.add_rule(FileDialogueRule(name="filedialogue"))
        grammar.load()
