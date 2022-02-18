import re
import logging

def validate_id(candidate_id):
    value = -1  # default return value if validation doesn't pass

    if bool(re.match('^[0-9a-zA-Z]{15}$',candidate_id)):
        value = 15
    elif bool(re.match('^[0-9a-zA-Z]{18}$',candidate_id)):
        if bool(re.match('^[a-z]{3}',candidate_id[-3:])):
            logging.warning("Last 3 digits of 18-digit ID not capitalized, "
                            "ID might have been mangled by another process.")
        value = 18

    return value

def get_caps(input_string):
    caps_nums = []
    for starts in [0, 5, 10]:
        caps_num = 0
        chars = input_string[starts:starts+5]
        for i in range(5):
            caps_num += 2**i if chars[i].isupper() else 0
        caps_nums.append(caps_num)

    # convert each char to base 32, represented by [A-Z0-5] in that order
    caps_chars = [str(i-26) if i > 25 else chr(i+ord('A')) for i in caps_nums]

    return ''.join(caps_chars)



def fifteen_to_eighteen(input_id):
    caps = get_caps(input_id)
    return input_id+caps


def eighteen_to_fifteen(input_id):
    first_fifteen = input_id[:15]
    caps = get_caps(first_fifteen)  # for casing validation
    if input_id[15:18].upper() != caps:
        logging.warning("Last 3 digits of 18-digit ID don't match computed"
                        "digits from casing of first 15 digits, "
                        "returning first 15 digits as-is.")
        # TODO: coerce the case of the first 15 digits to match the checksum
    else:
        output_id = first_fifteen

    return output_id


def convert(input_id):

    id_check = validate_id(input_id)  # length of ID if valid, else -1

    if id_check == 15:
        output_id = fifteen_to_eighteen(input_id)
    elif id_check == 18:
        output_id = eighteen_to_fifteen(input_id)
    else:
        logging.error("Invalid SFDC ID given; no conversion performed")
        output_id = input_id

    return output_id
