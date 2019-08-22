
from dragonfly import *
class CommandRule(MappingRule):
    mapping = {
        "splat [<n>]":Key("c-backspace:%(n)s"),
        "fly lease [<n>]": Key("c-left:%(n)s"),
        "fly ross [<n>]": Key("c-ross:%(n)s"),
        "lease [<n>]": Key("left:%(n)s"),
        "ross [<n>]": Key("right:%(n)s"),

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
# dict_cmd_sequence = Sequence([
#     Optional(RuleRef(command_rule)),
#     Repetition(Sequence([RuleRef(dictation_rule), RuleRef(command_rule)]), min=1, max=5),
#     Optional(RuleRef(dictation_rule)),
#     ], name="dict_cmd_sequence")

dict_cmd_sequence = Repetition(Alternative([RuleRef(dictation_rule), RuleRef(command_rule)]),
    min=1, max=10, name="dict_cmd_sequence")
# class SequenceRule(CompoundRule):
    # spec = "<dict_cmd_sequence>"
    # extras = [dict_cmd_sequence]
    # def _process_recognition(self, node, extras):
    #     for action in extras["dict_cmd_sequence"]:
    #         action.execute()

# dict_cmd_sequence = Sequence([
#     Optional(RuleRef(command_rule)),
#     Repetition(Sequence([RuleRef(dictation_rule), 
#     Repetition(RuleRef(command_rule), min=1, max=5)]), 
#     min=1, max=5),
#     Optional(RuleRef(dictation_rule)),
    # ], name="dict_cmd_sequence")
# command_repetition = Repetition(RuleRef(command_rule), min=1, max=5, name="command_repetition")
class SequenceRule(CompoundRule):
    spec = "<dict_cmd_sequence>"
    extras = [dict_cmd_sequence]
    # spec = "<command_repetition>"
    # extras = [command_repetition]
    def _process_recognition(self, node, extras):
        # repetition_actions = [a for thing in extras["dict_cmd_sequence"][1] for a in thing]
        # action_sequence = [extras["dict_cmd_sequence"][0]] + repetition_actions + [extras["dict_cmd_sequence"][2]]
        # action_sequence = [extras["command_repetition"]]
        # action_sequence = [extras["dict_cmd_sequence"][0]] + [a for a in extras["dict_cmd_sequence"][1]]  + [extras["dict_cmd_sequence"][2]]
        # action_sequence = [a for a in action_sequence if a is not None]
        for action in extras["dict_cmd_sequence"]:
            action.execute()

# grammar = Grammar("zurow")
# sequence_rule = SequenceRule()
# grammar.add_rule(sequence_rule)
# grammar.load()