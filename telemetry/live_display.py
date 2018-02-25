import tkinter as tk

from tkinter.font import Font

from .telemetry import TelemetryUserInterface


title = "Live Telemetry"
name_color = "white"
value_color = "#9dff8e"
background_color = "#222222"

font_family = "Segoe UI"
font_size = 12

window_width = 300
window_height = 600


class LiveTelemetryWindow(TelemetryUserInterface):
    def __init__(self):
        self.is_visible = False
        self.groups = []

        self.root = tk.Tk()
        self.root.configure(background=background_color)
        self.lb_names = tk.Label(self.root, text="", justify='left')
        self.lb_values = tk.Label(self.root, text="", justify='right')

        font = Font(self.root, family=font_family, size=font_size)

        self.lb_names.configure(font=font, background=background_color, foreground=name_color, anchor=tk.W)
        self.lb_values.configure(font=font, background=background_color, foreground=value_color, anchor=tk.E)

        self.lb_names.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.lb_values.grid(row=0, column=1)
        self.root.columnconfigure(0, weight=1)

        self.root.resizable(width=False, height=False)
        self.root.minsize(width=window_width, height=window_height)

        self.root.title(title)

    def logGroup(self, group_key):
        self.groups.append(group_key)

    def showWindow(self, value=True):
        self.is_visible = value

    def startMainLoop(self):
        self.root.mainloop()

    def update(self, telemetry):
        if self.is_visible:
            names_str = ""
            values_str = ""

            for group_key in self.groups:
                if group_key in telemetry:
                    group = telemetry[group_key]
                    names_str += "\n{}\n".format(str.upper(group['group_name']))
                    values_str += "\n\n"

                    data = group['data']
                    for key_name in data:
                        names_str += data[key_name]['name'] + ":\n"
                        val = data[key_name]['value']
                        unit = data[key_name]['unit']

                        if unit != "":
                            unit = " " + unit

                        if isinstance(val, float):
                            val = round(val, 3)

                        values_str += str(val) + unit + '\n'

            self.lb_names['text'] = names_str
            self.lb_values['text'] = values_str

            self.root.update()

    def getUserKey(self):
        return "live_display"


live_telemetry = LiveTelemetryWindow()
