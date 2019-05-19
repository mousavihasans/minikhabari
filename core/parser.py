import re


def isna_parser(content: str) -> list:
    # extract information and return data for saving in the News model
    # now just parse <p>, <strong>, <img>
    # todo: parse video
    # todo: parse other tags
    # return jsonify data

    array = []
    temp_var = ''
    open_tag = False
    # remove outer tag
    content = content[46:-6]

    # put tags and texts in arrays
    for char in content:
        if char == '<':
            open_tag = True
            if len(temp_var) > 0:
                array.append(temp_var)
                temp_var = ''
            temp_var += char
        elif char == '>':
            open_tag = False
            temp_var += char
            array.append(temp_var)
            temp_var = ''
        elif char == ' ':
            if len(temp_var) > 0 and not open_tag:
                array.append(temp_var)
                temp_var = ''
            else:
                temp_var += char
        else:
            temp_var += char

    # print(array)

    # parse array of tags and texts

    content = []
    current_tag = ''
    temp_array = []
    temp_dict = {}

    for item in array:

        if item[0:2] == '<p':
            # make a dict
            if len(temp_dict.keys()) == 0:
                temp_dict['p'] = []
                current_tag = 'p'

        elif item[0:3] == '</p':
            # close current dict and add it to array
            if len(temp_array) > 0:
                temp_dict[current_tag].append({'normal': ' '.join(temp_array)})
                content.append(temp_dict)
                temp_array = []
                temp_dict = {}

        elif item[0:7] == '<strong':
            if len(temp_array) > 0:
                temp_dict[current_tag].append({'normal': ' '.join(temp_array)})
                temp_array = []
        elif item[0:8] == '</strong':
            # add data
            temp_dict[current_tag].append({'bold': ' '.join(temp_array)})
            temp_array = []
        elif item[0:2] == '<a':
            # make a dict
            pass
        elif item[0:3] == '</a':
            # close current dict
            pass
        elif item[0:4] == '<img':
            if len(temp_array) > 0:  # todo: should save current tag state
                temp_dict[current_tag].append({'normal': ' '.join(temp_array)})
                temp_array = []
            matches = re.search('src="([^"]+)"', item)
            temp_dict[current_tag].append({'image': matches[0][4:]})
        elif item[0:4] == '<div':
            # video_link todo: handle video
            pass
        elif item[0:5] == '</div':
            pass
        else:
            # other tags and texts
            if item[0] == '<':
                pass
            else:
                temp_array.append(item)

    # print(content)
    return content
