



# It's worth noting that the name of this file, sample.py, will cause it to never run.
# You will have to rename it to "_sample.py".
# Putting an underscore as the first character of a grammar Python file will tell dragonfly
# that you want  this file to run all the time. Grammars that run all the time are good way to start.
# The alternative is making grammars for specific programs that only trigger when the programs are active.





from dragonfly import (BringApp, Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, WaitWindow, MappingRule, Text)

def my_function(n, text):
    print "put some Python logic here: "+str(text)
    
class MainRule(MappingRule):

    
    mapping = {
    # it is this section that you want to fiddle around with if you're new: mapping, extras, and defaults
               
               
    # in the next line, there are two things to observe:
    # the first is the use of parentheses and the pipe symbol (|)
    # --this lets me use either "lock dragon" or "deactivate" to trigger that command.
    # The next is the playback action, which lets me tell Dragon to simulate me speaking some words.
	'(lock Dragon | deactivate)':   Playback([(["go", "to", "sleep"], 0.0)]),
    
    # Here I'm using BringApp-- this is the same as typing what goes in between the parentheses
    # into the Windows command prompt, without the quotes and commas, like:
    # explorer C:\NatLink\NatLink\MacroSystem
    # -- (which would open Windows Explorer at the specified location). Anything you can do with the command line can be done this way
    "open natlink folder":          BringApp("explorer", "C:\NatLink\NatLink\MacroSystem"),
    
    # here I'm using the Key action to press some keys -- see the documentation here: http://dragonfly.readthedocs.org/en/latest/actions.html?highlight=key#module-dragonfly.actions.action_key
    "remax":                        Key("a-space/10,r/10,a-space/10,x"), 
    
    # here I'm chaining a bunch of different actions together to do a complex task
    "(show | open) documentation":  BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),
    
    # here I'm just saying one word to trigger some other words
    "hotel":                        Text("hotels are not cheap"),
    
    # If you need to do more complicated tasks, or use external resources, a function might be what you need.
    # note that here, I'm using extras: "n" and "text"
    # the angle brackets <> meaning I'm using an extra, and the square brackets [] mean that I don't have to speak that word, it's optional
    # advice: if you use an optional extra, like I am with "text", you should set a default value  in the defaults section down below
    # to trigger the following command, you would have to say the word "function" followed by a number between 1 and 1000
    '[use] function <n> [<text>]':    Function(my_function, extra={'n', 'text'}),
    
    
    
    }
    extras = [
              IntegerRef("n", 1, 1000),
              Dictation("text"),
              Choice("choice",
                    {"alarm": "alarm", "custom grid": "CustomGrid", "element": "e"
                    }),
             ]
    defaults = {"n": 1, 
               "text": "", 
               }

# this stuff is required too-- where I have the word "sample" below, each grammar file should have something unique
grammar = Grammar('sample')
grammar.add_rule(MainRule())
grammar.load()