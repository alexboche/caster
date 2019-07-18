#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Chrome

"""

from __future__ import print_function
import io
import os
import logging

from dragonfly import *

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.temporary import Store, Retrieve
from castervoice.lib.context import AppContext  
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

"""Code to visualize dragonfly trees written by Caspar Kreiger aka CasparK"""
# to get started, try `print get_grammar_complexity_tree(some_grammar, threshold=5)`.
# If you don't get any interesting output, turn up the threshold (max depth visualized) to something like 7 or 10 :)

class ComplexityNode(object):
    def __init__(self, item):
        self.item = item
        self.children = []
        self.total_descendents = 1


def build_complexity_tree(thing):
    node = ComplexityNode(thing)
    if isinstance(thing, Rule):
        children = [thing.element]
        element = thing.element
    elif isinstance(thing, RuleRef):
        children = [thing.rule.element]
    else:
        # thing is probably an Element
        children = thing.children

    for child in children:
        child_node = build_complexity_tree(child)
        node.children.append(child_node)
        node.total_descendents += child_node.total_descendents

    if isinstance(thing, Alternative):
        node.children = sorted(node.children, reverse=False,
                               key=lambda node: str(node.item))
        node.children = sorted(node.children, reverse=True,
                               key=lambda node: node.total_descendents)

    return node


def get_rule_complexity_tree(rule, depth_threshold=10, complexity_threshold=10):
    def render_complexity_tree(node, current_depth):
        pluralized_children = "children" if len(
            node.children) != 1 else "child"
        node_name = "  " * current_depth + \
            "- %-50s %-6d" % (node.item, node.total_descendents)

        #if current_depth >= depth_threshold:
         #   return ""
        #elif node.total_descendents <= complexity_threshold:
            #return "%s (+ %3d uncomplex direct %s)" % (node_name, len(node.children), pluralized_children)

        if (isinstance(node.item, Integer)
                or isinstance(node.item, Compound) and node.total_descendents <= 2):
            children_repr = " (+ %3d trivial direct %s)" % (
                len(node.children), pluralized_children)
        elif False and current_depth + 1 == depth_threshold and node.total_descendents > 1:
            children_repr = " (+ %3d truncated direct %s)" % (
                len(node.children), pluralized_children)
        else:
            children_repr = ""
            for child in node.children:
                child_repr = render_complexity_tree(child, current_depth + 1)
                if len(child_repr) > 0:
                    children_repr += "\n" + child_repr

        return node_name + children_repr

    try:
        tree = build_complexity_tree(rule)
        return render_complexity_tree(tree, 0)
    except Exception:
        logging.exception("failed to build complexity tree")
        return ""


def get_grammar_complexity_score(grammar):
    try:
        return sum([build_complexity_tree(r).total_descendents for r in grammar.rules if r.exported])
    except Exception:
        logging.exception("failed to build grammar complexity score")
        return 0


def get_grammar_complexity_tree(grammar, threshold=5):
    rules_all = grammar.rules
    rules_top = [r for r in grammar.rules if r.exported]
    rules_imp = [r for r in grammar.rules if r.imported]
    text = ("%s: %d rules (%d exported, %d imported):" % (
        grammar, len(rules_all), len(rules_top), len(rules_imp),
    ))
    for rule in rules_top:
        text += "\n%s" % get_rule_complexity_tree(rule, threshold)
    return text



class ChromeRule(MergeRule):
    pronunciation = "google chrome"
    mapping = {
        
        "new window":
            R(Key("c-n")),
        "(new incognito window | incognito)":
            R(Key("cs-n")),
        "new [tab] [<n>]":
            R(Key("c-t")*Repeat(extra="n")),
        "reopen tab [<n>]":
            R(Key("cs-t"))*Repeat(extra="n"),
        "close tab [<n>]":
            R(Key("c-w"))*Repeat(extra='n'),
        "close all tabs":
            R(Key("cs-w")),
        "(nab | next tab) [<n>]":
            R(Key("c-tab"))*Repeat(extra="n"),
        "(lab | previous tab) [<n>]":
            R(Key("cs-tab"))*Repeat(extra="n"),
        "new tab that":
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        "<nth> tab":
            R(Key("c-%(nth)s") ),
        "last tab":
            R(Key("c-9")),
        "second last tab":
            R(Key("c-9, cs-tab")),
        "go back [<n>]":
            R(Key("a-left/20"))*Repeat(extra="n"),
        "go forward [<n>]":
            R(Key("a-right/20"))*Repeat(extra="n"),
        "zoom in [<n>]":
            R(Key("c-plus/20"))*Repeat(extra="n"),
        "zoom out [<n>]":
            R(Key("c-minus/20"))*Repeat(extra="n"),
        "zoom reset":
            R(Key("c-0")),
        "super refresh":
            R(Key("c-f5")),
        "switch focus [<n>]":
            R(Key("f6/20"))*Repeat(extra="n"),
        "[find] next match [<n>]":
            R(Key("c-g/20"))*Repeat(extra="n"),
        "[find] prior match [<n>]":
            R(Key("cs-g/20"))*Repeat(extra="n"),
        "[toggle] caret browsing":
            R(Key("f7")),
              # now available through an add on, was a standard feature
        "home page":
            R(Key("a-home")),
        "[show] history":
            R(Key("c-h")),
        "address bar":
            R(Key("c-l")),
        "show downloads":
            R(Key("c-j")),
        "add bookmark":
            R(Key("c-d")),
        "bookmark all tabs":
            R(Key("cs-d")),
        "[toggle] bookmark bar":
            R(Key("cs-b")),
        "[show] bookmarks":
            R(Key("cs-o")),
        "switch user":
            R(Key("cs-m")),
        "chrome task manager":
            R(Key("s-escape")),
        "[toggle] full-screen":
            R(Key("f11")),
        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "deny notification":
            R(Key("as-a")),
        "developer tools":
            R(Key("f12")),
        "view [page] source":
            R(Key("c-u")),
        "resume":
            R(Key("f8")),
        "step over":
            R(Key("f10")),
        "step into":
            R(Key("f11")),
        "step out":
            R(Key("s-f11")),

        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),

        "google that":
            R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),

        "wikipedia that":
            R(Store(space="+", remove_cr=True) + Key("c-t") + Text("https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),

        "duplicate tab":
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        "duplicate window":
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        "extensions":
            R(Key("a-f/20, l, e/15, enter")),
        "(menu | three dots)":
            R(Key("a-f")),
        "settings":
            R(Key("a-f/5, s")),
        "downloads":
            R(Key("c-j")),
        "chrome task manager":
            R(Key("s-escape")),
        "clear browsing data":
            R(Key("cs-del")),
        "developer tools":
            R(Key("cs-i")),
        "more tools":
            R(Key("a-f/5, l")),
         "[<click_by_voice_options>] <numbers>": R(Key("cs-space/30")
            + Text("%(numbers)d:%(click_by_voice_options)s") + Key("enter"), 
            rdescript="click link with click by voice options"),
        "go <numbers> <dictation>": Key("cs-space/30") + Text("%(numbers)d")
            + Key("enter") + Text("%(dictation)s"),
        "hit <numbers> <dictation>": 
            Key("cs-space/30") + Text("%(numbers)d") + Key("enter")
            + Text("%(dictation)s") + Key("enter"),
        "hide hints": R(Key("cs-space/30")+Text(":-")+Key("enter"),
             rdescript="hide click by voice hints (i.e. numbers)"),
        "show hints": R(Key("cs-space/30")+Text(":+")+Key("enter"),
            rdescript="show click by voice hints (i.e. numbers)"),
    }
    extras = [
        Choice(
            "click_by_voice_options",
            {
                "focus": "f",
                "click": "c",
                "push": "b",  # open as new tab but don't go to it
                "tab": "t",  # open as new tab and go to it
                "window": "w",
                "hover": "h",
                "link": "k",
                "copy": "s",
            }),
        Choice("nth", {
            "first": "1",
            "second": "2",
            "third": "3",
            "fourth": "4",
            "fifth": "5",
            "sixth": "6",
            "seventh": "7",
            "eighth": "8",
        }),
        Dictation("dictation"),
        IntegerRefST("n", 1, 10),
        IntegerRefST("m", 1, 10),
        IntegerRefST("numbers", 0, 1000),
    ]
    defaults = {"n": 1, "dict": "", "click_by_voice_options": "c"}


#---------------------------------------------------------------------------

context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=context)

if settings.SETTINGS["apps"]["chrome"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(ChromeRule())
    else:
        rule = ChromeRule(name="chrome")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()




# print grammar complexity tree for Chrome grammar
with io.open(os.path.expanduser('~/visualize_chrome'), 'wb') as f:
    print('------------------', file=f)
    print(get_grammar_complexity_tree(grammar), file=f)

  
# print grammar complexity tree for all non-CCR grammars 
with io.open(os.path.expanduser('~/visualize_all_non_ccr_grammars'), 'wb') as f:
    engine = engines.get_engine()
    for wrapper in engine._grammar_wrappers.values():
        print(wrapper.grammar._name)
        print(get_grammar_complexity_tree(wrapper.grammar), file=f)
        print('------------------', file=f)  
        print('------------------', file=f)  

# print grammar complexity tree for caster CCR grammars
    # This part Isn't Working anymore though use do not sure exactly why
    
# mr = control.nexus().merger
# grs = mr._grammars
# with io.open(os.path.expanduser('~/debugout_caster_ccr_grammars/'), 'wb') as f:
#     # this is giving length zero right now, so it's an empty list
#     print(len(grs), file=f) 
#     for g in grs:
#           print(g._name, file=f)
#     for g in grs:
#           print(g._name, file=f)
               
#           print(get_grammar_complexity_tree(g), file=f)
#           print('------------------', file=f)
#     for name, rule in control.nexus().merger._app_rules.items():
#         print(name, file=f)
#         print(get_rule_complexity_tree(rule), file=f)   
#         print('-------------------------', file=f)
    