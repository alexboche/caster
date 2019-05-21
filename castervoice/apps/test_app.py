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
    clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clip[0]
    temp_for_previous_clipboard_item = clip[1]
    replaced_phrase = str(replaced_phrase)
    replacement_phrase = str(replacement_phrase) 
    new_text = replace_phrase_with_phrase(selected_text, replaced_phrase, replacement_phrase, left_right)
    if not new_text:
        # replaced_phrase not found
        # method 1: paste selected text over itself, sometimes a little slower but works in texstudio
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        # method 2: unselect text by using the arrow keys, a little faster but does not work in texstudio
        # if left_right == "left":
        #     Key("right").execute()
        # if left_right == "right":
        #     Key("left").execute()
        # put previous clipboard item back in the clipboard
        Pause("20").execute()
        pyperclip.copy(temp_for_previous_clipboard_item)
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
    clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clip[0]
    temp_for_previous_clipboard_item = clip[1]
    phrase = str(phrase)
    new_text = remove_phrase_from_text(selected_text, phrase, left_right)
    if not new_text:
        # phrase not found
        # method 1: paste selected text over itself, sometimes a little slower but works in texstudio
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        # method 2: unselect text by using the arrow keys, a little faster but does not work in texstudio
        # if left_right == "left":
        #     Key("right").execute()
        # if left_right == "right":
        #     Key("left").execute()
        # put previous clipboard item back in the clipboard
        Pause("20").execute()
        pyperclip.copy(temp_for_previous_clipboard_item)
        return
    pyperclip.copy(new_text)
    Key("c-v").execute()

    if left_right == "right":
        offset = len(new_text)
        Key("left:%d" %offset).execute()
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)


def move_until_phrase(left_right, before_after, phrase, number_of_lines_to_search):
    """ move until the close end of the phrase"""
    # set default for before_after
    if before_after == None:
        print("hello")
        if left_right  == "left":
            before_after = "after"
        if left_right == "right":
            before_after = "before"
    # print(before_after)

    clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clip[0]
    temp_for_previous_clipboard_item = clip[1]
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        # phrase not found
        # method 1: paste selected text over itself, sometimes a little slower but works in texstudio
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        # method 2: unselect text by using the arrow keys, a little faster but does not work in texstudio
        # if left_right == "left":
        #     Key("right").execute()
        # if left_right == "right":
        #     Key("left").execute()
        # put previous clipboard item back in the clipboard
        Pause("20").execute()
        pyperclip.copy(temp_for_previous_clipboard_item)
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    # Approach 1: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    # comments below indicate the other approach
    # Key("c-v").execute()
    # if before_after == "before":
    #     selected_text_to_the_right_of_phrase = selected_text[left_index :]    
    # if before_after == "after":
    #     selected_text_to_the_right_of_phrase = selected_text[right_index :]
    # multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
    # if before_after  == "before":
    #     offset = len(selected_text) - left_index - multiline_offset_correction
    # if before_after == "after":
    #     offset = len(selected_text) - right_index - multiline_offset_correction
    # Key("left:%d" %offset).execute()

    
    # Approach 2: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    if right_index < round(len(selected_text))/2:
        # it's faster to approach phrase from the left
        Key("left").execute() # unselect text and place cursor on the left side of selection 
        if before_after  == "before":
            offset_correction = selected_text[: left_index].count("\r\n")
            offset = left_index - offset_correction
        if before_after  == "after":
            offset_correction = selected_text[: right_index].count("\r\n")
            offset = right_index - offset_correction
        Key("right:%d" %offset).execute()
    else:
        # it's faster to approach phrase from the right
        Key("right").execute() # unselect text and place cursor on the right side of selection
        if before_after  == "before":
            offset_correction = selected_text[left_index :].count("\r\n")
            offset = len(selected_text) - left_index - offset_correction
        if before_after  == "after":
            offset_correction = selected_text[right_index :].count("\r\n")
            offset = len(selected_text) - right_index - offset_correction
        Key("left:%d" %offset).execute()
        

    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)

def select_phrase(phrase, left_right, number_of_lines_to_search):
    clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clip[0]
    temp_for_previous_clipboard_item = clip[1]
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        # method 2: unselect text by using the arrow keys, a little faster but does not work in texstudio
        # if left_right == "left":
        #     Key("right").execute()
        # if left_right == "right":
        #     Key("left").execute()
        # put previous clipboard item back in the clipboard
        Pause("20").execute()
        pyperclip.copy(temp_for_previous_clipboard_item)
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    
    # Approach 1: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    # comments below indicate the other approach
    Key("c-v").execute()
    multiline_movement_correction = selected_text[right_index :].count("\r\n")
    movement_offset = len(selected_text) - right_index - multiline_movement_correction
    Key("left:%d" %movement_offset).execute()
    multiline_selection_correction = selected_text[left_index : right_index].count("\r\n")
    selection_offset = len(selected_text[left_index : right_index]) - multiline_selection_correction
    Key("s-left:%d" %selection_offset).execute()



    # Approach 2: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    # if right_index < round(len(selected_text))/2:
    #     # it's faster to approach phrase from the left
    #     Key("left").execute() # unselect text and place cursor on the left side of selection 
    #     multiline_movement_offset_correction = selected_text[: left_index].count("\r\n")
    #     movement_offset = left_index - multiline_movement_offset_correction
    #     # move to the left side of the phrase
    #     Key("right:%d" %movement_offset).execute()
    #     # select phrase
    #     multiline_selection_offset_correction = selected_text[left_index : right_index].count("\r\n")
    #     selection_offset = len(phrase) - multiline_selection_offset_correction
    #     Key("s-right:%d" %selection_offset).execute()
    # else:
    #     # it's faster to approach phrase from the right
    #     Key("right").execute() # unselect text and place cursor on the right side of selection
    #     multiline_movement_offset_correction = selected_text[left_index :].count("\r\n")
    #     movement_offset = len(selected_text) -  left_index - multiline_movement_offset_correction
    #     # move to the left side of the phrase
    #     Key("left:%d" %movement_offset).execute()
    #     # select phrase
    #     multiline_selection_offset_correction = selected_text[left_index : right_index].count("\r\n")
    #     selection_offset = len(phrase) - multiline_selection_offset_correction
    #     Key("s-right:%d" %selection_offset).execute()
    
    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)

def select_until_phrase(left_right, phrase, before_after, number_of_lines_to_search):
    """ the selection will include the phrase unless it is punctuation"""
    # set default for before_after
    if not before_after:
        if left_right  == "left":
            before_after = "after"
        if left_right == "right":
            before_after = "before"

    
    clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clip[0]
    temp_for_previous_clipboard_item = clip[1]
    phrase = str(phrase)
    match = get_start_end_position(selected_text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        # method 2: unselect text by using the arrow keys, a little faster but does not work in texstudio
        # if left_right == "left":
        #     Key("right").execute()
        # if left_right == "right":
        #     Key("left").execute()
        # put previous clipboard item back in the clipboard
        Pause("20").execute()
        pyperclip.copy(temp_for_previous_clipboard_item)
        return
    left_index, right_index = get_start_end_position(selected_text, phrase, left_right)
    
# Approach 1: paste the selected text over itself rather than simply unselecting. A little slower but works Texstudio
    # comments below indicate the other method
    # Key("c-v").execute()  
    # if left_right == "left":
    #     if before_after == "before": 
    #         selected_text_to_the_right_of_phrase = selected_text[left_index :]    
    #         multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
    #         offset = len(selected_text) - left_index - multiline_offset_correction
            
    #     if before_after == "after":
    #         selected_text_to_the_right_of_phrase = selected_text[right_index :]
    #         multiline_offset_correction = selected_text_to_the_right_of_phrase.count("\r\n")
    #         offset = len(selected_text) - right_index - multiline_offset_correction
        
    #     Key("s-left:%d" %offset).execute()
    # if left_right == "right":
    #     multiline_movement_correction = selected_text.count("\r\n")
    #     movement_offset = len(selected_text) - multiline_movement_correction
        
    #     if before_after == "before":
    #         multiline_selection_correction = selected_text[: left_index].count("\r\n")
    #         selection_offset = left_index - multiline_movement_correction
    #     if before_after == "after":
    #         multiline_selection_correction = selected_text[: right_index].count("\r\n")
    #         selection_offset = right_index

        # # move cursor to original position
        # Key("left:%d" %movement_offset).execute()
        # # select text
        # Key("s-right:%d" %selection_offset).execute()
    
    # Approach 2: unselect using arrow keys rather than pasting over the existing text. (a little faster) does not work texstudio
    if left_right == "left":
        Key("right").execute() # unselect text and move to left side of selection
        if before_after == "before":
            multiline_correction = selected_text[left_index :].count("\r\n")
            offset = len(selected_text) - left_index - multiline_correction
        if before_after == "after":
            multiline_correction = selected_text[right_index :].count("\r\n")
            offset = len(selected_text) - right_index - multiline_correction
        Key("s-left:%d" %offset).execute()
    if left_right == "right": 
        Key("left").execute() # unselect text and move to the right side of selection
        if before_after == "before":
            multiline_correction = selected_text[: left_index].count("\r\n")
            offset = left_index - multiline_correction
        if before_after == "after":
            multiline_correction = selected_text[: right_index].count("\r\n")
            offset = right_index - multiline_correction
        Key("s-right:%d" %offset).execute()


    # put previous clipboard item back in the clipboard
    Pause("20").execute()
    pyperclip.copy(temp_for_previous_clipboard_item)



def delete_until_phrase(text, phrase, left_right, before_after):
    match = get_start_end_position(text, phrase, left_right)
    if match:
        left_index, right_index = match
    else:
        return
    # the spacing below may need to be tweaked
    if left_right == "left":
        if before_after == "before":
            # if text[-1] == " ":
            #     return text[: left_index] + " "
                return text[: left_index]

        else: # todo: handle before-and-after defaults better
            if text[-1] == " ":
                return text[: right_index] + " "
            else:
                return text[: right_index]
    if left_right == "right":
        if before_after == "after":
            return text[right_index :]
        else:
            if text[0] == " ":
                return " " + text[left_index :]
            else:
                return text[left_index :]

def copypaste_delete_until_phrase(left_right, phrase, number_of_lines_to_search, before_after):
    clip = select_text_and_return_it(left_right, number_of_lines_to_search)
    selected_text = clip[0]
    temp_for_previous_clipboard_item = clip[1]
    
    phrase = str(phrase)
    new_text = delete_until_phrase(selected_text, phrase, left_right, before_after)
    if not new_text:
        # phrase not found
        Key("c-v").execute()
        if left_right == "right":
            print("right")
            Key("left:%d" %len(selected_text)).execute()
        # method 2: unselect text by using the arrow keys, a little faster but does not work in texstudio
        # if left_right == "left":
        #     Key("right").execute()
        # if left_right == "right":
        #     Key("left").execute()
        # put previous clipboard item back in the clipboard
        Pause("20").execute()
        pyperclip.copy(temp_for_previous_clipboard_item)
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
        "Tiger": Key("up:0"),

        
        # "(replace|to) <lease_ross> [<number_of_lines_to_search>] <dictation> (with|to) <dictation2>":
        #     R(Function(copypaste_replace_phrase_with_phrase,
        #                dict(dictation="replaced_phrase", dictation2="replacement_phrase", lease_ross="left_right")),
        #       rdescript="Core: replace text to the left or right of the cursor"),
        
        # "remove <lease_ross> [<number_of_lines_to_search>] <dictation>":
        #     R(Function(copypaste_remove_phrase_from_text,
        #                dict(dictation="phrase", lease_ross="left_right")),
        #       rdescript="remove chosen phrase to the left or right of the cursor"),
        # "remove lease [<number_of_lines_to_search>] <left_character>":
        #     R(Function(copypaste_remove_phrase_from_text,
        #                dict(left_character="phrase"),
        #                left_right="left"),
        #       rdescript="remove chosen character to the left of the cursor"),
        # "remove ross [<number_of_lines_to_search>] <right_character>":
        #     R(Function(copypaste_remove_phrase_from_text,
        #                dict(right_character="phrase"),
        #                left_right="right"),
        #       rdescript="remove chosen character to the right of the cursor"),

        # problem: sometimes Dragon thinks the before-and-after variable is part of dictation.      
        # "move <lease_ross> [<number_of_lines_to_search>] [<before_after>] <dictation>":
        #     R(Function(move_until_phrase,
        #                dict(dictation="phrase", lease_ross="left_right")),
        #       rdescript="move to chosen phrase to the left or right of the cursor"),
        # "move lease [<before_after>] [<number_of_lines_to_search>] <left_character>":
        #     R(Function(move_until_phrase,
        #                dict(left_character="phrase"),
        #                left_right="left"),
        #       rdescript="move to chosen character to the left of the cursor"),
        # "move ross [<before_after>] [<number_of_lines_to_search>] <right_character>":
        #     R(Function(move_until_phrase,
        #                dict(right_character="phrase"),
        #                left_right="right"),
        #       rdescript="move to chosen character to the right of the cursor"),
        # "grab <lease_ross> [<number_of_lines_to_search>] <dictation> ":
        #     R(Function(select_phrase, dict(dictation="phrase", lease_ross="left_right")),
        #          rdescript="select chosen phrase"),
        # "grab lease [<number_of_lines_to_search>] <left_character>":
        #     R(Function(select_phrase, dict(left_character="phrase"), left_right="left"),
        #     rdescript="select chosen character to the left"),
        # "grab ross [<number_of_lines_to_search>] <right_character>":
        #     R(Function(select_phrase, dict(right_character="phrase"), left_right="right"),
        #     rdescript="select chosen character to the right"),
        
        # "grab <lease_ross> [<number_of_lines_to_search>] until <dictation> ":
        #     R(Function(select_until_phrase, dict(dictation="phrase", lease_ross="left_right")),
        #          rdescript="select until chosen phrase (inclusive)"),
        # "grab lease [<number_of_lines_to_search>] until <left_character>":
        #     R(Function(select_until_phrase, dict(left_character="phrase"), left_right="left"),
        #     rdescript="select left until chosen character"),
        # "grab ross [<number_of_lines_to_search>] until  <right_character>":
        #     R(Function(select_until_phrase, dict(right_character="phrase"), left_right="right"),
        #     rdescript="select right until chosen character"),
        # "wipe <lease_ross> [<number_of_lines_to_search>] [<before_after>] <dictation>":
        #     R(Function(copypaste_delete_until_phrase,
        #                dict(dictation="phrase", lease_ross="left_right")),
        #       rdescript="delete left until chosen phrase (exclusive)"),
        # "wipe lease [<number_of_lines_to_search>] [<before_after>] <left_character>":
        #     R(Function(copypaste_delete_until_phrase,
        #                dict(left_character="phrase"),
        #                left_right="left"),
        #       rdescript="delete left until chosen character (exclusive)"),
        # "wipe ross [<number_of_lines_to_search>] [<before_after>] <right_character>":
        #     R(Function(copypaste_delete_until_phrase,
        #                dict(right_character="phrase"), 
        #                left_right="right"),
        #       rdescript="delete left until chosen character"),
        




        
        
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
        "number_of_lines_to_search": 0,}


# context = utils.MultiAppContext(relevant_apps={})
# grammar = Grammar("test_rule", context=context)

# rule = GlobalTestRule(name="globaltestrule")
# gfilter.run_on(rule)
# grammar.add_rule(rule)
# grammar.load()




