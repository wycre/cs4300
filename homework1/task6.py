import os

def count_words(filename):
    file = open(filename, "r")
    text = file.read()
    words = text.split()
    return len(words)


"""Lines 11-14 written by ChatGPT https://chatgpt.com/share/67acfc16-ccb0-8011-8108-e2c1c5afec22"""
if __name__ == "__main__":
    text_files = [f for f in os.listdir() if f.endswith(".txt")]
    for file in text_files:
        print(f"{file}: {count_words(file)} words")
