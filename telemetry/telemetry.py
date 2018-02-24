telemetry = {}
telemetry_providers = {}


class TelemetryProviderInterface:
    def getProviderKey(self):
        return NotImplemented

    def provideTelemetry(self):
        """
        Returns telemetry data.
        Use telemetry.TelemetryBuilder to create the object
        :return:
        """
        return NotImplemented


class TelemetryBuilder:
    """
    Creates the object to be returned by a provider's provideTelemetry method.
    """
    def __init__(self, group_name):
        self.data = {}
        self.group_name = group_name

    def addData(self, key, value):
        self.data[key] = value
        return self

    def build(self):
        return self.group_name + "_telemetry", self.data


def addProvider(provider: TelemetryProviderInterface):
    telemetry_providers[provider.getProviderKey()] = provider


def removeProvider(provider: TelemetryProviderInterface):
    del telemetry_providers[provider.getProviderKey()]


def update():
    # Reset telemetry
    global telemetry
    telemetry = {}

    for k in telemetry_providers.keys():  # type: TelemetryProviderInterface
        data = telemetry_providers[k].provideTelemetry()
        telemetry[data[0]] = data[1]

    print(telemetry)
