from dragonfly import Function, Key, Text, Mouse, Pause, Dictation, Choice, Grammar 
import subprocess
import pyperclip
import re 
import io


from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.apps import utils
from castervoice.apps import reloader
from castervoice.apps import reloader

punctuation_list = []

def get_start_end_position(text, phrase, left_right):
    if left_right == "left":
        if phrase in punctuation_list:
            pattern = re.escape(phrase)
        else:
            # the \b avoids e.g. matching 'and' in 'land' but seems to allow e.g. matching 'and' in 'hello.and'
            # for matching purposes use lowercase

            pattern = r"\b" + re.escape(phrase.lower()) + r"\b"            
        
        if not re.search(pattern, text.lower()):
            # replaced phase not found
            print("'{}' not found".format(phrase))
            return
        
        match_iter = re.finditer(pattern, text.lower())
        match_list = [(m.start(), m.end()) for m in match_iter]
        last_match = match_list[-1]
        left_index, right_index = last_match


    if left_right == "right":
        # if replaced phrase is punctuation, don't require a word boundary for match
        if phrase in punctuation_list:
            pattern = re.escape(phrase.lower())
        # phrase contains a word
        else:
            pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        match = re.search(pattern, text.lower())
        if not match:
            print("'{}' not found".format(phrase))
            return
        else:
            left_index, right_index = match.span()
    return (left_index, right_index)


def select_text_and_return_it(left_right, number_of_lines_to_search):
    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()
    Pause("30").execute()
    if left_right == "left":
        Key("s-home, s-up:%d, s-home, c-c" %number_of_lines_to_search).execute()
    if left_right == "right":
        Key("s-end, s-down:%d, s-end, c-c" %number_of_lines_to_search).execute()
    Pause("60").execute()
    selected_text = pyperclip.paste()
    return (selected_text, temp_for_previous_clipboard_item)

def replace_phrase_with_phrase(text, replaced_phrase, replacement_phrase, left_right):
    match = get_start_end_position(text, replaced_phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
    return text[: left_index] + replacement_phrase + text[right_index:] 
    


def copypaste_replace_phrase_with_phrase(replaced_phrase, replacement_phrase, left_right, number_of_lines_to_search):
    clipboard = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clipboard[0]
    temp_for_previous_clipboard_item = clipboard[1]
    replaced_phrase = str(replaced_phrase)
    replacement_phrase = str(replacement_phrase) 
    new_text = replace_phrase_with_phrase(selected_text, replaced_phrase, replacement_phrase, left_right)
    if not new_text:
        # replaced_phrase not found
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        return
    
    pyperclip.copy(new_text)
    Key("c-v").execute()
    if number_of_lines_to_search < 20: 
        # only put the cursor back in the right spot if the number of lines to search is fairly small
        if left_right == "right":
            offset = len(new_text)
            Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)

def remove_phrase_from_text(text, phrase, left_right):
    match = get_start_end_position(text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
        
    # if the "phrase" is punctuation, just remove it, but otherwise remove an extra space adjacent to the phrase
    if phrase in punctuation_list:
        return text[: left_index] + text[right_index:] 
    else:
        return text[: left_index - 1] + text[right_index:] 


def copypaste_remove_phrase_from_text(phrase, left_right, number_of_lines_to_search):
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)[0]
    temp_for_previous_clipboard_item = select_text_and_return_it(left_right, number_of_lines_to_search)[1]
    
    phrase = str(phrase)
    new_text = remove_phrase_from_text(selected_text, phrase, left_right)
    if not new_text:
        # phrase not found
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        return

    pyperclip.copy(new_text)
    Key("c-v").execute()

    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)


def move_until_phrase(left_right, before_after, phrase):
    """ move until the close end of the phrase"""

    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()
    
    if left_right == "left":
        Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end, c-c/2").execute()
    selected_text = pyperclip.paste()
    Pause("10").execute()
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        Key("c-v").execute()
        if left_right == "right":
            offset = len(selected_text)
            Key("left:%d" %offset).execute()
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    
    # # I am using the method of pasting over the existing text rather than simply unselecting because of some weird behavior in texstudio
    # # comments below indicate the other method
    Key("c-v").execute() # paste selected text over itself, thus unselecting the text and putting the cursor on the right side of the selection
    if left_right == "left":
        if before_after == "before":
            # move the cursor before the phrase
            if left_index < round(len(selected_text)/2):
                # it's faster to approach the phrase from the left
                Key("home").execute() # unselect text and move to the end of the line
                offset = left_index
                Key("right:%d" %offset).execute()
            else:
                # it's faster to approach the phrase from the right
                offset = len(selected_text) - left_index
                Key("left:%d" %offset).execute()
        else:
            # before_after == "after" or before_after == None, so move the cursor to after the phrase
            if right_index < round(len(selected_text)/2):
                # it's faster to approach the phrase from the left
                Key("home").execute() # unselect text and move to the end of the line
                offset = right_index
                Key("home, right:%d" %offset).execute()
            else:
                # it's faster to approach the phrase from the right
                offset = len(selected_text) - right_index
                Key("left:%d" %offset).execute()
                       
    if left_right == "right":
        # since we are using the method of pasting the selected text over itself, we cannot use any optimization about approaching from left versus right.
        if before_after == "after":
            offset = len(selected_text) - right_index
        else:
            offset = len(selected_text) - left_index
        Key("left:%d" %offset).execute()



    
    # Alternative method: simply unselect rather than pasting over the existing text. (a little faster) does not work texstudio
    # if left_right == "left":
    #     if before_after == "before":
    #         # we will move the cursor before the phrase
    #         if left_index < round(len(selected_text)/2):
    #             # it's faster to approach the phrase from the left
    #             Key("home").execute() # unselect text and move to the end of the line
    #             offset = left_index
    #             Key("right:%d" %offset).execute()
    #         else:
    #             # it's faster to approach the phrase from the right
    #             Key("right").execute() # unselect text and move to the left side of the selection
    #             offset = len(selected_text) - left_index
    #             Key("left:%d" %offset).execute()
    #     else:
    #         # before_after == "after" or before_after == None, so move the cursor after the phrase
    #         if right_index < round(len(selected_text)/2):
    #             # it's faster to approach the phrase from the left
    #             Key("home").execute() # unselect text and move to the end of the line
    #             offset = right_index
    #             Key("home, right:%d" %offset).execute()
    #         else:
    #             # it's faster to approach the phrase from the right
    #             Key("end").execute() # unselect text and move to the end of the line
    #             offset = len(selected_text) - right_index
    #             Key("left:%d" %offset).execute()
                       
    # if left_right == "right":
        
    #     if before_after == "after":
    #         # we will move the cursor after the phrase
    #         if right_index > round(len(selected_text)/2):
    #             # it's faster to approach the phrase from the right
    #             Key("end").execute()
    #             offset = len(selected_text) - right_index
    #             Key("left:%d" %offset).execute()
    #         else:
    #             # it's faster to approach the phrase from the left
    #             Key("left").execute() # unselect text and move to left side of selection                
    #             offset = right_index
    #             Key("right:%d" %offset).execute()
    #         offset = right_index
    #     else:
    #         # before_after == "before" or before_after == None, so move the cursor before the phrase
    #         if left_index > round(len(selected_text)/2):
    #             # it's faster to approach the phrase from the right
    #             Key("end").execute() # unselect text and move to end of line
    #             offset = len(selected_text) - left_index
    #             Key("left:%d" %offset).execute()
    #         else:
    #             # it's faster to approach the phrase from the left
    #             Key("left").execute() # unselect text and move to left side of selection
    #             offset = left_index
    #             Key("right:%d" %offset).execute()
    
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)

def select_until_phrase(left_right, phrase):
    """ the selection will include the phrase unless it is punctuation"""
    # temporarily store previous clipboard item
    temp_for_previous_clipboard_item = pyperclip.paste()

    
    if left_right == "left":
        Key("s-home, c-c/2").execute()
    if left_right == "right":
        Key("s-end, c-c/2").execute()
    selected_text = pyperclip.paste()
    Pause("10").execute()
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        Key("c-v").execute()
        if left_right == "right":
            offset = len(selected_text)
            Key("left:%d" %offset).execute()
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    
    # I am using the method of pasting over the existing text rather than simply unselecting because of some weird behavior in texstudio
    # comments below indicate the other method
    # Key("c-v").execute()
    # if left_right == "left":
    #     offset = len(selected_text) - left_index
    #     # make noninclusive if it's punctuation
    #     if phrase in punctuation_list:
    #         offset -= 1
    #     Key("s-left:%d" %offset).execute()
    # if left_right == "right":
    #     len_selected_text = len(selected_text)
    #     offset = right_index
    #     # make noninclusive if it's punctuation
    #     if phrase in punctuation_list:
    #         offset -= 1
    #     Key("left:%d" %len_selected_text).execute()
    #     Key("s-right:%d" %offset).execute()
    
    # # alternative method: simply unselects text rather than pasting over the text. a little faster but does not work in tex studio
    if left_right == "left":
        Key("right").execute() # unselect text
        offset = len(selected_text) - left_index
        # make noninclusive if it's punctuation 
        if phrase in punctuation_list:
            offset -= 1
        Key("s-left:%d" %offset).execute()
    if left_right == "right":
        Key("left").execute() # unselect text
        Key("s-right:%d" %(right_index -1)).execute() # make noninclusive if it's punctuation 
   
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)



def delete_until_phrase(text, phrase, left_right):
    match = get_start_end_position(text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
    if left_right == "left":
        return text[: right_index]
    if left_right == "right":
        return text[right_index :]

def copypaste_delete_until_phrase(left_right, phrase, number_of_lines_to_search):
    selected_text = select_text_and_return_it(left_right, number_of_lines_to_search)[0]
    temp_for_previous_clipboard_item = select_text_and_return_it(left_right, number_of_lines_to_search)[1]
    
    phrase = str(phrase)
    new_text = delete_until_phrase(selected_text, phrase, left_right)
    if not new_text:
        # phrase not found
        Key("c-v").execute()
        if left_right == "right":
            Key("left:%d" %len(selected_text)).execute()
        return

    # put modified text on the clipboard
    pyperclip.copy(new_text)
    Key("c-v").execute()

    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)



class GlobalTestRule(MergeRule):
    pronunciation = "global alex rule"


    mapping = {
        "bathroom": R(Text("de"), rdescript="red blue"), 

        




        
        
    }
    extras = [
        Dictation("dict"),
        Dictation("dictation"),
        Dictation("dictation2"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        IntegerRefST("m", 1, 100),
        IntegerRefST("wait_time", 1, 1000),
        IntegerRefST("number_of_lines_to_search", 1, 50),
        Choice("character_sequence", {
            "comma": ",",
        }),
        Choice("left_character", {
            "prekris": "(",
            "brax": "[",
            "angle": "<",
            "curly": "{",
            "quotes": '"',
            "single quote": "'",
            "comma": ",",
            "period": ".",
            "questo": "?",
            "backtick": "`",
        }),
        Choice("right_character", {
            "prekris": ")",
            "brax": "]",
            "angle": ">",
            "curly": "}",
            "quotes": '"',
            "single quote": "'",
            "comma": ",",
            "period": ".",
            "questo": "?",
            "backtick": "`",
        }),
        Choice("lease_ross", {
            "lease": "left",
            "ross": "right",
        }),
        Choice("before_after", {
            "before": "before",
            "after": "after",
        }),
        
        
    ]
    defaults = {"n": 1, "m": 1, "spec": "", "dict": "", "text": "", "mouse_button": "", 
        "horizontal_distance": 0, "vertical_distance": 0, 
        "lease_ross": "left",
        "before_after": None,
        "number_of_lines_to_search": 5,}

        




context = utils.MultiAppContext(relevant_apps={})
grammar = Grammar("test_rule", context=context)

rule = GlobalTestRule(name="globaltestrule")
gfilter.run_on(rule)
grammar.add_rule(rule)
grammar.load()




