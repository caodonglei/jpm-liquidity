
class Configer:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self._version = 0

    def has_update(self):
        return False

    def get_config(self) -> dict:
        """ get config of the module
        """
        return {'TOKENS': {'btc_usdt': {'interval': 1}}}