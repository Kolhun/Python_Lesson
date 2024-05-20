import easyocr


def text_recognition(file_path):
    reader = easyocr.Reader(['ru', "en"], gpu=False)
    result = reader.readtext(file_path)
    return result


def main():
    print(text_recognition(file_path='phone.jpg'))


if __name__ == '__main__':
    main()
