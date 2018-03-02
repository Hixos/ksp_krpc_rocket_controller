from .telemetry import TelemetryUserInterface

import os
import csv


class TelemetryLogger(TelemetryUserInterface):
    def __init__(self):
        self.providers = []
        self.inited = {}
        self.files = {}
        self.csv_writers = {}

    def logProvider(self, provider_key):
        file_name = os.path.join("logs", provider_key + ".csv")
        #path = os.path.join(os.path.abspath(__file__), file_name)
        file = open(file_name, 'w', newline='')
        self.providers.append(provider_key)

        self.inited[provider_key] = False
        self.files[provider_key] = file

    def update(self, telemetry, providers, T, dt):
        for provider_key in self.providers:
            # Check if we wrote the header for the provider:
            data_keys = [k['key'] for k in providers[provider_key]['data']]
            if not self.inited[provider_key]:
                writer = csv.DictWriter(self.files[provider_key], delimiter=',', quotechar='"',
                                        quoting=csv.QUOTE_NONNUMERIC, fieldnames=data_keys)  # type:csv.DictWriter
                self.csv_writers[provider_key] = writer
                writer.writeheader()
                self.inited[provider_key] = True

            if provider_key in telemetry and telemetry[provider_key] is not None:
                data = {}
                for i in range(0, len(data_keys)):
                    data[data_keys[i]] = telemetry[provider_key][i]

                self.csv_writers[provider_key].writerow(data)

    def close(self):
        for k in self.files.keys():
            self.files[k].close()

telemetry_logger = TelemetryLogger()