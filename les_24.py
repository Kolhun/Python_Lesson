
from pprint import pprint

file = open("les_24_text.txt", mode="rb")
file_content = file.read();
file.close()
pprint(file_content)