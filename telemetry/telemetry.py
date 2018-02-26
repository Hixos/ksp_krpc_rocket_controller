class TelemetryManager:
    class InvalidTelemetryDataError(Exception):
        pass

    class ProviderAlreadyRegisteredError(Exception):
        pass

    def __init__(self):
        self.providers = {}
        self.users = {}

        self.telemetry = {}

    def registerUser(self, user_key, user):
        self.users[user_key] = user

    def removeUser(self, user_key):
        del self.users[user_key]

    def registerProvider(self, provider_key, provider_name, provider):
        """
        Register a telemetry provider. On every update, each registered provider's getTelemetry method will be called.
        :param provider_key: Unique key for the provider
        :param provider_name: Human readable name for this provider
        :param provider: The provider object

        """
        if provider_key in self.providers:
            raise TelemetryManager.ProviderAlreadyRegisteredError("Telemetry provider {} already registered."
                                                                  .format(provider_key))

        self.providers[provider_key] = {'name': provider_name, 'object': provider, 'data': provider.describeData()}

    def collectTelemetry(self):
        for key in self.providers.keys():
            provider = self.providers[key]
            tel = provider['object'].getTelemetry()

            # We let the provider return None from getTelemetry when there's no useful telemetry (EG: an idle state)
            if tel is not None and len(tel) != len(provider['data']):
                raise TelemetryManager.InvalidTelemetryDataError("Invalid number of telemetry data provided by {}"
                                                                 .format(key))

            self.telemetry[key] = tel

    def join(self, telemetry, provider):
        """
        Joins telemetry and providers in a single dictionary
        """
        for k in provider.keys():
            if telemetry[k] is not None:
                del provider[k]['object']
                for i in range(0, len(provider[k]['data'])):
                    provider[k]['data'][i]['value'] = telemetry[k][i]
            else:
                del provider[k]

        return provider

    def update(self):
        self.collectTelemetry()

        for k in self.users.keys():
            self.users[k].update(self.join(self.telemetry, self.providers))

    def close(self):
        for k in self.users.keys():
            self.users[k].close()


class TelemetryProviderInterface:
    """
    Interface for a telemetry provider.
    """
    def describeData(self):
        """
        Returns a description of the telemetry data.
        This method is called once upon the provider registration in the TelemetryManager.
        The type of data provided must not change afterwards.

        :return: A description of telemetry data returned by the  getTelemetry method.
        Must be a list of objects created with TelemetryDescriptionBuilder
        """
        return NotImplemented

    def getTelemetry(self):
        """
        Return a list containing the current telemetry data, in the order specified by describeData
        """
        return NotImplemented


class TelemetryDescriptionBuilder:
    def __init__(self):
        self.desc = []

    def addData(self, key, name, unit):
        """
        Add a new data
        :param key: Unique key
        :param name: Human readable name
        :param unit: Unit of measurement
        """
        self.desc.append({'key': key, 'name': name, 'unit': unit})
        return self

    def build(self):
        return self.desc


class TelemetryUserInterface:
    def update(self, telemetry):
        return NotImplemented

    def close(self):
        pass
