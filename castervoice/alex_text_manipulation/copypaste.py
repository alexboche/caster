import io
import pyperclip


def pyper_delete_until_character_sequence(character_sequence, left_right):
        text = text = pyperclip.paste()
        new_text = delete_until_character_sequence(text, character_sequence, left_right)
        pyperclip.copy(new_text)
        

def delete_until_character_sequence(text, character_sequence, left_right):
    if left_right == "left":

        character_sequence_start_position = text.rfind(character_sequence)
        new_text_start_position = character_sequence_start_position 
        new_text = text[:new_text_start_position]
        return new_text
    if left_right == "right":
        
        character_sequence_start_position = text.find(character_sequence)
        new_text_start_position = character_sequence_start_position + len(character_sequence)
        new_text = text[new_text_start_position:]
        return new_text
    

expected = "my name is Alex"
print(delete_until_character_sequence("my name is Alex, what is your name", ",", "left"))
assert delete_until_character_sequence("my name is Alex, what is your name", ",", "left") == expected
# assert pyper_delete_until_character_sequence(",", "left") == expected


def delete_until(left_string, right_string, previous_next_both, text_pattern):
    previous_location = left_string.rfind("text_pattern")
    next_location = right_string.find("text_pattern")
    # I am making it inclusive for now
    new_left_string = left_string[:previous_location + 1]
    new_right_string = right_string[next_location:]
    pass



# storage file
file_name = r"C:\NatLink\NatLink\MacroSystem\castervoice\alex_text_manipulation\storage.txt"
    

def save_clipboard_to_file():
    s = pyperclip.paste()
    file_name = r"C:\NatLink\NatLink\MacroSystem\castervoice\alex_text_manipulation\storage.txt"
    with io.open(file_name, 'w') as f:
        f.write(s)

def delete_current_sentence(left_string, right_string):
    # cursor_position  = len(left_string)
    previous_period_location = left_string.rfind(".")
    next_period_location = right_string.find(".")

    # new_left_string includes the period
    new_left_string = left_string[:previous_period_location + 1]

    # new_right_string includes the space after the period.
    new_right_string = right_string[next_period_location + 1:]

    full_string = new_left_string + new_right_string
    return full_string

def deleter():
    file_name = r"C:\NatLink\NatLink\MacroSystem\castervoice\alex_text_manipulation\storage.txt"
    left_string = ""
    with io.open(file_name, 'r') as f:
        left_string = f.read()
    right_string = pyperclip.paste()
    pyperclip.copy(delete_current_sentence(left_string, right_string))
def test_delete_sentence():
    left_string = "When the day that you happen to know is Wednesday starts off by sounding like Sunday, there is something seriously wrong somewhere. I felt like that from the moment I look. And yet, when I started functioning a little more sharply, I'm escape. After all the odds were that it was I who was wrong, not every"
    right_string = "one else, though I did not see how that could be. I went on waiting, teamed with doubt. But presently I had my first bit of objective evidence, distant clock struck what sounded to me like eight. I listened hard and suspiciously peer soon another clock began, on a loud, decisive note. In a leisurely fashion it gave an indisputable eight. Then I knew that things were awry."

    result = delete_current_sentence(left_string, right_string)

    expected = "When the day that you happen to know is Wednesday starts off by sounding like Sunday, there is something seriously wrong somewhere. I felt like that from the moment I look. I went on waiting, teamed with doubt. But presently I had my first bit of objective evidence, distant clock struck what sounded to me like eight. I listened hard and suspiciously peer soon another clock began, on a loud, decisive note. In a leisurely fashion it gave an indisputable eight. Then I knew that things were awry."
    print(result)
    assert expected == result


