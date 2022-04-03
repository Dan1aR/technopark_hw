""" Contains function to parse your valid html """
# CONSTS
OPEN_TAG = '_open'
VALUE_TAG = '_value'
CLOSE_TAG = '_close'
START_OF_SEQUENCE = 'SOS'

open_tags_count = {}
max_data_len = 0


def open_tag_process(tag):
    """ Counts amount of every tag """
    global open_tags_count
    if tag in open_tags_count:
        open_tags_count[tag] += 1
    else:
        open_tags_count[tag] = 1
    return open_tags_count


def data_process(content):
    """ Calculates max len of data """
    global max_data_len
    max_data_len = max(max_data_len, len(content))
    return max_data_len


def close_tag_process():
    """ Finds most frequent tag """
    global open_tags_count
    return max(open_tags_count, key=lambda x: open_tags_count[x])


def parse_html(html_str, open_tag_callback, data_callback, close_tag_callback):
    """ Generate dict from html """
    def generate_dict(idx=0):
        """ Returns len(stack_tags), ['SOS': PARSED HTML HERE]"""
        nonlocal stack_tags

        _tag, content = stack_tags[idx]
        if _tag == OPEN_TAG:
            next_idx, html_el = generate_dict(idx+1)
            while stack_tags[next_idx][0] != CLOSE_TAG:
                next_idx, sub_el = generate_dict(next_idx)
                html_el += sub_el
            html_el = {content: html_el}
            idx, content = next_idx+1, [html_el]

        if _tag == VALUE_TAG:
            idx, content = idx+1, [content]

        return idx, content

    stack_tags = [(OPEN_TAG, START_OF_SEQUENCE)]

    sub_str = ""
    stack = []
    for char in html_str:
        if char == "<":
            data_callback(sub_str)
            if sub_str and not sub_str.isspace():
                stack_tags.append((VALUE_TAG, sub_str.strip()))
            sub_str = ""
            stack.append(char)
        elif char == "/":
            stack[-1] += char
        elif char == ">":
            if stack[-1] == "<":
                open_tag_callback(sub_str)
                stack_tags.append((OPEN_TAG, sub_str.strip()))
            if stack[-1] == "</":
                close_tag_callback()
                stack_tags.append((CLOSE_TAG, sub_str.strip()))
            stack.append(char)
            sub_str = ""
        else:
            sub_str += char

    data_callback(sub_str)
    if sub_str and not sub_str.isspace():
        stack_tags.append((VALUE_TAG, sub_str.strip()))

    stack_tags.append((CLOSE_TAG, START_OF_SEQUENCE))
    return generate_dict()[-1][0][START_OF_SEQUENCE]


if __name__ == "__main__":
    HTML = """
        <h1>They were not!</h1>
        <p> <h2> Their memory serves as an example to us all! </h2>
        The courageous fallen! The anguished fallen! </p>
        <p> Their lives have meaning because </p>
        <p> we the living refuse to forget them! </p>
        <div>
        <class> <a> And as we ride to certain death, </a>
        <a> we trust our successors to do the same for us! </a>
        <a> Because my soldiers do not buckle or yield </a>
        <a> when faced with the cruelty of this world! </a> </class>
        </div>
        <h3> My soldiers push forward! </h3>
        <h2> My soldiers scream out! </h2>
        <h1> My soldiers RAAAAAGE! </h1>
    """

    print(parse_html(HTML, open_tag_process, data_process, close_tag_process))

    print(f"Open tags statistic: {open_tags_count}")
    print(f"Max data len = {max_data_len}")
    print(f"Tags most frequent: {close_tag_process()}")
