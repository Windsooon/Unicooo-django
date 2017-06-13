import re


def text_contain_xss(text):
    pattern = re.compile("^((?!\'|\"|<|>).)*$")
    return pattern.match(text)
