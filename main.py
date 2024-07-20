import json
import math
import os
import sys
from datetime import datetime
from threading import Timer

import plyer
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, ThreeLineListItem, ThreeLineIconListItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.tooltip import MDTooltip
import android

Window.size = (415, 620)


class Lock_Screen(MDScreen):
    def login(self):
        app = MDApp.get_running_app().root
        a = self.ids.password.text
        if a.lower() == "password":
            try:
                with open("tasks.json", "r") as file:
                    data = json.load(file)
                    tasks_list = data
            except:
                data = []
                with open("tasks.json", "w") as file:
                    json.dump(data, file)
                    tasks_list = data

            for tasks in tasks_list:
                try:
                    with open(f"{tasks}.json", "r") as file:
                        data = json.load(file)
                        notify = data.get("notify", 0)

                except:
                    pass

                try:
                    with open(f"{tasks}.json", "r") as ffile:
                        data = json.load(ffile)
                        date = data.get("date", "")
                        time = data.get("time", "")
                except:
                    pass

                def fire_alarm(name, data):
                    plyer.notification.notify(title="Task Update", message=name)

                try:
                    ready_datetime = f"{date} {time}"
                    format_string = "%Y-%m-%d %H:%M:%S"
                    ready_date = datetime.strptime(ready_datetime, format_string)

                    datetime_obj = datetime(ready_date.year, ready_date.month, ready_date.day, ready_date.hour,
                                            ready_date.minute, ready_date.second)

                    current_date = datetime.today()

                    ring_seconds = (datetime_obj - current_date)
                    x = ring_seconds.total_seconds()
                    c = math.ceil(x)
                    print(c)

                    if c >= 0:
                        name = (tasks, {"key": "value"})
                        timer = Timer(c, fire_alarm, args=name)

                        timer.start()
                    else:
                        name = (tasks, {"key": "value"})
                        timer = Timer(0, fire_alarm, args=name)

                        timer.start()
                except:
                    pass

            app.get_screen("home").ids.create_list.trigger_action(0)

            self.manager.current = "home"
            self.ids.password.text = ""

        else:
            self.ids.password.hint_text = "Wrong Password"

    def alarm(self, dt):
        plyer.notification.notify(title="Task", message=self.tasks)
        print(self.tasks)

    def delete(self):
        self.ids.password.text = ""


class Content_B(MDScreen):
    def delete(self):
        app = MDApp.get_running_app().root
        task = app.get_screen("home").ids.clicked_task.text
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                tasks_list = data
        except:
            pass

        tasks_list.remove(task)

        try:
            data = tasks_list
            with open("tasks.json", "w") as file:
                json.dump(data, file)
        except:
            pass

        os.remove(f"{task}.json")

        app.get_screen("home").ids.create_list.trigger_action(0)
        app.get_screen("home").ids.dismiss_b.trigger_action(0)

    def done(self):
        app = MDApp.get_running_app().root
        app.get_screen("home").ids.done.trigger_action(0)
        app.get_screen("home").ids.dismiss_b.trigger_action(0)


class Content_A(MDScreen):
    def add(self):
        task = self.ids.task.text

        def fire_alarm():
            # Perform your alarm action here
            plyer.notification.notify(title="Task Update", message=task)
        app = MDApp.get_running_app().root
        app.get_screen("home").ids.list.clear_widgets()

        try:
            with open("tasks.json", "r") as afile:
                data = json.load(afile)
                tasks_list = data
        except:
            data = []
            with open("tasks.json", "w") as bfile:
                json.dump(data, bfile)
                tasks_list = data

        tasks_list.append(task)

        try:
            data = tasks_list
            with open("tasks.json", "w") as cfile:
                json.dump(data, cfile)
        except:
            pass

        try:
            data = {"date": self.task_date, "time": self.task_time}
            with open(f"{task}.json", "w") as dfile:
                json.dump(data, dfile)

        except:
            data = {"date": "", "time": ""}
            with open(f"{task}.json", "w") as efile:
                json.dump(data, efile)

        try:
            with open(f"{task}.json", "r") as ffile:
                data = json.load(ffile)
                date = data.get("date", "")
                time = data.get("time", "")
        except:
            pass
        try:
            ready_datetime = f"{date} {time}"
            format_string = "%Y-%m-%d %H:%M:%S"
            ready_date = datetime.strptime(ready_datetime, format_string)

            datetime_obj = datetime(ready_date.year, ready_date.month, ready_date.day, ready_date.hour, ready_date.minute, ready_date.second)

            current_date = datetime.today()

            ring_seconds = abs(datetime_obj - current_date)
            x = ring_seconds.total_seconds()
            c = math.ceil(x)

            timer = Timer(c, fire_alarm)
            timer.start()

        except:
            pass

        app.get_screen("home").ids.create_list.trigger_action(0)
        self.cancel()

    def alarm(self, dt):
        screen_manager = MDApp.get_running_app().root
        task = self.ids.task.text
        plyer.notification.notify(title="Task", message=task)
        print("ALARM")

    def cancel(self):
        MDApp.get_running_app().root.get_screen("home").ids.dismiss.trigger_action(0)

    def show_date_picker(self):
        date_picker = MDDatePicker(title="Select Task Date", title_input="Task Date")
        date_picker.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_picker.open()

    def show_time_picker(self):
        time_picker = MDTimePicker(title="Set Timer")
        time_picker.bind(on_save=self.save_time, on_cancel=self.cancel_time)
        time_picker.open()

    def cancel_time(self, instance, time):
        pass

    def save_time(self, instance, time):
        self.task_time = str(time)
        screen_manager = MDApp.get_running_app().root
        pass

    def on_cancel(self, instance, date):
        pass

    def on_save(self, instance, date, date_range):
        screen_manager = MDApp.get_running_app().root
        a = str(date)
        self.task_date = a
        # datetime_obj = datetime(date.year, date.month, date.day, 9, 0, 0)
        #
        # self.ids.cday.text = a
        #
        # current_date = datetime.today()
        #
        # ring_seconds = abs(datetime_obj - current_date)
        # x = ring_seconds.total_seconds()
        # c = math.ceil(x)
        # print(c)
        # self.ids.notice.text = str(c)
        # # Clock.schedule_once(self.alarm, c)
        # self.save_data()


class Tip(MDIconButton, MDTooltip):
    pass


class Home(MDScreen):
    def add(self):
        self.dialog = MDDialog(
            type="custom",
            _anim_duration=.25,
            widget_style='android',
            content_cls=Content_A(),
            radius=[18, 18, 18, 18],
            size_hint=[.9, None],
            opacity=1
        )
        self.dialog.open()

    def dismiss(self):
        self.dialog.dismiss()

    def create_list(self):
        app = MDApp.get_running_app().root
        app.get_screen("home").ids.list.clear_widgets()
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                tasks_list = data
        except Exception as e:
            print(e)

        for tasks in tasks_list:
            try:
                with open(f"{tasks}.json", "r") as file:
                    data = json.load(file)
                    date = data.get("date", "")
                    time = data.get("time", "")
                    bg_color =  data.get("color", )
            except Exception as e:
                print(e)

            list_item = ThreeLineListItem(text=tasks,
                                          secondary_text=date,
                                          tertiary_text=time,
                                          divider_color=[.4, 0, .8, 1],
                                          bg_color= bg_color
                                          )
            list_item.bind(
                on_release=lambda instance, item=list_item: self.enter(item))

            self.ids.list.add_widget(list_item)

    def enter(self, item):
        self.colored = item.bg_color
        # item.bg_color = [0, 0, 0, .4]
        app = MDApp.get_running_app().root
        self.items = item.text

        self.dialogs = MDDialog(
            type="custom",
            _anim_duration=.25,
            widget_style='android',
            content_cls=Content_B(),
            radius=[18, 18, 18, 18],
            size_hint=[.9, None],
            opacity=1
        )
        self.dialogs.open()
        app.get_screen("home").ids.clicked_task.text = item.text

    def done(self):
        try:
            with open(f"{self.items}.json", "r") as file:
                self.data = json.load(file)
                colour = self.data.get("color", )
                if colour != [0, 0, 0, 0.4]:
                    self.data["color"] = [0, 0, 0, 0.4]
                else:
                    self.data["color"] = [0, 0, 0, 0]
        except Exception as e:
            print(e)

        try:
            with open(f"{self.items}.json", "w") as file:
                json.dump(self.data, file)
        except Exception as e:
            print(e)
        self.create_list()

    def dismiss_b(self):
        self.dialogs.dismiss()


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        global sm
        scr_manager = ScreenManager
        self.theme_cls.primary_palette = 'DeepPurple'
        return 0


# TaskApp().run()
if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))

        MainApp().run()
    except Exception as e:
        print(e)
        input("Press enter.")
