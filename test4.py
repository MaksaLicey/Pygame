class A:
    def __init__(self):
        print("A start")
        self.running = True
        self.open_class = False
        self.cycle()

    def fake__init__(self):
        self.running = True
        # self.open_class = False
        self.cycle()

    def cycle(self):
        while self.running:
            str1 = input()
            if str1 == "A close":
                self.running = False
                self.open_class = True
                print("А was close")
            elif str1 == "stop all":
                self.running = False
                self.open_class = False

    def stop(self):
        self.open_class = False


class B:
    def __init__(self, flag1=False):
        print("B start")
        self.running = True
        self.open_class = False
        self.cycle()

    def fake__init__(self):
        self.running = True
        # self.open_class = False
        self.cycle()

    def cycle(self):
        while self.running:
            str1 = input()
            if str1 == "B close":
                self.running = False
                self.open_class = True
                print("B was close")
            elif str1 == "stop all":
                self.running = False
                self.open_class = False

    def stop(self):
        self.open_class = False


def game_nanager():
    app1 = A()
    app2 = None
    while True:
        print("1")
        if app1.open_class:
            if app2 is None:
                app2 = B()
            else:
                app2.fake__init__()
            app1.stop()
        elif app2.open_class:
            app1.fake__init__()
            app2.stop()
        elif not app1.open_class and not app2.open_class:
            print("end cycle of classes")
            break


game_nanager()
