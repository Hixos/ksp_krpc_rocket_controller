from .telemetry import TelemetryUserInterface

import csv

class TelemetryLogger(TelemetryUserInterface):
    def __init__(self, filename, telemetry_ukey):
        self.telemetry_key = telemetry_ukey
        self.file_name = filename
        self.groups = []

        self.file = open(self.file_name, 'w' newline='')
        self.writer = csv.writer(self.file, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_NONNUMERIC)  # type: csv.DictWriter

    def logGroups(self, *group_keys):
        self.groups.append(group_keys)

    def update(self, telemetry):
        super().update(telemetry)

    def getRow(self, telemetry):
        row = []
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

    def getUserKey(self):
        return self.telemetry_key

    def finalize(self):
        self.file.close()

