
from dragonfly import *

class CommandRule(MappingRule):
    mapping = {
        "splat [<n>]":Key("c-backspace:%(n)s"),
        }
    extras = [IntegerRef("n", 1, 10)]
    defaults = {"n":1}
command_rule = CommandRule()
class DictationRule(MappingRule):
    mapping = {
        "<dictation>": Text("%(dictation)s "), # adding a trailing space
    }
    extras = [ Dictation("dictation") ]
dictation_rule = DictationRule()
dict_cmd_sequence = Sequence([
    Optional(RuleRef(command_rule)),
    Repetition(Sequence([RuleRef(dictation_rule), RuleRef(command_rule)]), min=1, max=16),
    Optional(RuleRef(dictation_rule)),
    ], name="dict_cmd_sequence")
class SequenceRule(CompoundRule):
    spec = "<dict_cmd_sequence>"
    extras = [dict_cmd_sequence]
    def _process_recognition(self, node, extras):
        action_sequence = [extras["dict_cmd_sequence"][0]] + [a for pair in extras["dict_cmd_sequence"][1] for a in pair] + [extras["dict_cmd_sequence"][2]]
        # action_sequence = [extras[0][0]] + [a for a in pair for pair in extras[0][1]] + [extras[0][2]]
        # action_sequence = [extras["dictation_command_sequence"][0] + [a for a in extras["dictation_command_sequence"][1]] + extras["dictation_command_sequence"][2]]
        action_sequence = [a for a in action_sequence if a is not None]
        for action in action_sequence:
            action.execute()

context = AppContext(executable="texmaker")
grammar = Grammar("zurow", context=context)
sequence_rule = SequenceRule()
# dictation_rule = DictationRule()
# command_rule = CommandRule()
grammar.add_rule(sequence_rule)
# grammar.add_rule(math_rule)
# grammar.add_rule(math_dictation_rule)
grammar.load()