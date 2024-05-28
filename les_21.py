import time
import hashlib


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16)
        self.age = age


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, login, password):
        hashed_password = int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16)
        for user in self.users:
            if user.nickname == login and user.password == hashed_password:
                self.current_user = user
                return
        print("Пользователь не найден")

    def register(self, nickname, password, age):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} зарегистрирован")

    def log_out(self):
        self.current_user = None

    def add(self, *videos):
        for video in videos:
            if video.title not in [v.title for v in self.videos]:
                self.videos.append(video)

    def get_videos(self, search_word):
        search_word = search_word.lower()
        matching_videos = [video.title for video in self.videos if search_word in video.title.lower()]
        return matching_videos

    def watch_video(self, title):
        if self.current_user is None:
            print("Войдите в аккаунт чтобы смотреть видео")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return
                for i in range(video.duration):
                    print(f"Просмотр {i + 1} секунды")
                    time.sleep(1)
                video.time_now = 0
                print("Конец видео")
                return
        print("Видео не найдено")
