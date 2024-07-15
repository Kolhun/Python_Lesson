import threading
import time
import datetime


tm_not_threading = datetime.timedelta()
def witeWords(word_count : int, file_name : str):
    global tm_not_threading
    start_time = datetime.datetime.now()
    with open(file_name, "w") as file:
        for i in range(word_count):
            file.write(f"\nКакое-то слово № {i}")
    time.sleep(0.1)
    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    tm_not_threading += execution_time

witeWords(10, "example1.txt")
witeWords(30, "example2.txt")
witeWords(200, "example3.txt")
witeWords(100, "example4.txt")
print(f"Время на один поток заняло {tm_not_threading}")
tm_not_threading = datetime.timedelta()

thread1 = threading.Thread(target=witeWords, args=(10, "example1.txt"))
thread2 = threading.Thread(target=witeWords, args=(30, "example2.txt"))
thread3 = threading.Thread(target=witeWords, args=(200, "example3.txt"))
thread4 = threading.Thread(target=witeWords, args=(100, "example4.txt"))

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()

print(f"Время на несколько потоков заняло {tm_not_threading}")
