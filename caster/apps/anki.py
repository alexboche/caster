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
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class AnkiRule(MergeRule):
    pronunciation = "anki"

    mapping = {
        "add": R(Key("a"), rdescript="Anki: Add"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefST("n", 1, 10),
    ]
    defaults = {"n": 1, "dict": "nothing"}


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
        executable = executable.lower()

        if not self._relevant_apps:
            # If no apps are relevant, then all apps will match.

            if self._log_match:
                self._log_match.debug("%s: Match." % self)
            return True

        for app in self._relevant_apps:
            if app.lower() in executable:
                if self._log_match:
                    self._log_match.debug("%s: Match." % self)
                return True

        return False




context = MultiAppContext(relevant_apps={'anki', 'word'})
grammar = Grammar("anki", context=context)

if settings.SETTINGS["apps"]["anki"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AnkiRule())
    else:
        rule = AnkiRule(name="anki")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
