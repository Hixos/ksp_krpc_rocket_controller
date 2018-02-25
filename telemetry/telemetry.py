telemetry = {}
telemetry_providers = {}
telemetry_users = {}


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


class TelemetryUserInterface:
    def getUserKey(self):
        return NotImplemented

    def update(self, telemetry):
        return NotImplemented


class TelemetryBuilder:
    """
    Creates the object to be returned by a provider's provideTelemetry method.
    """
    def __init__(self, group_key, group_name):
        self.group_key = group_key
        self.group_name = group_name
        self.data = {}

    def addData(self, key, name, value, unit=""):
        self.data[key] = {'name': name,
                          'value': value,
                          'unit': unit}
        return self

    def build(self):
        return self.group_key, {'group_name': self.group_name, 'data': self.data}


def addProvider(provider: TelemetryProviderInterface):
    telemetry_providers[provider.getProviderKey()] = provider


def removeProvider(provider: TelemetryProviderInterface):
    del telemetry_providers[provider.getProviderKey()]


def addUser(user: TelemetryUserInterface):
    telemetry_users[user.getUserKey()] = user


def removeUser(user: TelemetryUserInterface):
    del telemetry_users[user.getUserKey()]


def update():
    # Reset telemetry
    global telemetry
    telemetry = {}

    for k in telemetry_providers.keys():
        data = telemetry_providers[k].provideTelemetry()
        if data is not None:
            telemetry[data[0]] = data[1]

    for k in telemetry_users.keys():
        telemetry_users[k].update(telemetry)
