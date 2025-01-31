def count_words():
    file = open("task6_read_me.py", "r") # why is it supposed to be a python file if it's plaintext?
    text = file.read()
    words = text.split()
    return len(words)
