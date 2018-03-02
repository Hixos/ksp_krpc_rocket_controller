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
        self.providers = []

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

    def displayProvider(self, provider_key, priority=10):
        """
        Adds a telemetry provider to the live display
        :param provider_key: The provider key used in the TelemetryManager
        :param priority: Providers with a low priority number will be displayed first in the list
        """
        self.providers.append((priority, provider_key))
        self.providers.sort(key=lambda tup: tup[0])

    def showWindow(self, value=True):
        self.is_visible = value

    def startMainLoop(self):
        self.root.mainloop()

    def update(self, telemetry, providers, T, dt):
        if self.is_visible:
            names_str = ""
            values_str = ""

            for provider in reversed(self.providers):
                provider_key = provider[1]
                if provider_key in telemetry:
                    data = telemetry[provider_key]
                    desc = providers[provider_key]
                    if data is not None:
                        names_str += "\n{}\n".format(str.upper(desc['name']))
                        values_str += "\n\n"

                        for i in range(0, len(data)):
                            names_str += desc['data'][i]['name'] + ":\n"
                            val = data[i]
                            unit = desc['data'][i]['unit']

                            if unit != "":
                                unit = " " + unit

                            if isinstance(val, float):
                                val = round(val, 3)

                            values_str += str(val) + unit + '\n'

            self.lb_names['text'] = names_str
            self.lb_values['text'] = values_str

            self.root.update()


live_telemetry = LiveTelemetryWindow()
