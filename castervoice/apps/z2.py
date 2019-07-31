from dragonfly import *
import nsformat
formatting_state = None
def format_dictation(dictation, input_state):
        formatted_output, output_state = nsformat.formatWords(str(dictation), state=input_state)
        formatted_output = str(formatted_output)
        Text("%(formatted_output)s").execute()
        global formatting_state 
        formatting_state = output_state

        
class CommandRule(MappingRule):
    mapping = {
        "splat [<n>]":Key("c-backspace:%(n)s"),
        "fly lease [<n>]": Key("c-left:%(n)s"),
        "fly ross [<n>]": Key("c-right:%(n)s"),
        "lease [<n>]": Key("left:%(n)s"),
        "ross [<n>]": Key("right:%(n)s"),

        }
    extras = [IntegerRef("n", 1, 10)]
    defaults = {"n":1}
command_rule = CommandRule()
class DictationRule(MappingRule):
    
    mapping = {
        # "<dictation>": Text("%(dictation)s "), # adding a trailing space
        "<dictation>": Function(format_dictation, input_state=formatting_state)
    }
    extras = [ Dictation("dictation") ]
dictation_rule = DictationRule()

dict_cmd_sequence = Repetition(Alternative([RuleRef(dictation_rule), RuleRef(command_rule)]),
    min=1, max=10, name="dict_cmd_sequence")

class SequenceRule(CompoundRule):
    spec = "<dict_cmd_sequence>"
    extras = [dict_cmd_sequence]
    def _process_recognition(self, node, extras):
        for action in extras["dict_cmd_sequence"]:
                action.execute()

grammar = Grammar("zurow")
sequence_rule = SequenceRule()
grammar.add_rule(sequence_rule)
grammar.load()