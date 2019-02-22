#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Chrome and Firefox

"""
#---------------------------------------------------------------------------
import dragonfly
from dragonfly import (Grammar, Choice, Context, AppContext, Dictation, Key, Text, Repeat, BringApp)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class AlexRule(MergeRule):
    pronunciation = 'alex'
    mapping = {
        "press key <my_key>": Key("%(a)s"),
        "print these words <my_words>": Text("words I said: %(my_words)s"),
        By the way I find the following commands really useful especially when I'm using a headset or long-range  table Mike. The first to ignore whatever you said. The 3rd ignores whatever you said and turned off the mic.
"<my_words> (Peru)": Text(''),
"(talk | talking) <my_words>": Text(''),
" <my_words> (Brazil)": Key('f1'),

        " <my_words> (Peru)": Text(''),
        " <my_words> (Brazil)": Key('f1'),

      #  "snooze [<my_words>]": Key('f1'),
                                "KB start": BringApp(r"C:\Program Files (x86)\KnowBrainer\KnowBrainer Professional 2017\KBPro.exe"),
       # "begin pycharm": BringApp(r"C:\Program Files\JetBrains\PyCharm Community Edition 2018.2.1\bin")
    }

    extras = [
        Choice("my_key", {
            "arch": "a",
            "brav": "b",
            "char": "c"
        }),
        Dictation("my_words"),
    ]

#---------------------------------------------------------------------------




class MultiAppContext(Context):
    # ----------------------------------------------------------------------
    # Initialization methods.

    def __init__(self, relevant_apps=None, title=None, exclude=False):
        Context.__init__(self)

        if relevant_apps is None:
            self._relevant_apps = None
        else:
            self._relevant_apps = set(relevant_apps)

        self._title = title
        self._exclude = bool(exclude)

        self._str = "%s, %s, %s" % (self._relevant_apps, self._title,
                                    self._exclude)

    # ----------------------------------------------------------------------
    # Matching methods.

    def matches(self, executable, title, handle):
        return True




context = MultiAppContext()
grammar = Grammar("alex", context=context)

if settings.SETTINGS["apps"]["alex"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AlexRule())
    else:
        rule = AlexRule(name="alex")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
