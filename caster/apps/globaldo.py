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
from dragonfly import (Grammar, Context, AppContext, Dictation, Key, Text, Repeat, Function)

from caster.lib import control
from caster.lib import settings
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

from . import utils
from . import reloader

#---------------------------------------------------------------------------

def eight(*args, **kwargs):
    return 88888888888

class GlobalContext(Context):

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
        self._log_match.debug("%s: Match." % self)
        return True

bingo bingo
class GlobalRule(MergeRule):

    pronunciation = "global"

    mapping = {
        "bingo":  Text('hello')),
    }



context = GlobalContext()
grammar = Grammar("global", context=context)

if settings.SETTINGS["apps"]["global"]:
    rule = GlobalRule(name="global")
    gfilter.run_on(rule)
    grammar.add_rule(rule)
    grammar.load()
