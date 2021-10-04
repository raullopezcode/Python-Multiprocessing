from config.BreastConfig import config as BreastConfig
class ConfigFactory:
    @staticmethod
    def from_name(name: str):
        if name == 'breast':
            return BreastConfig
        
        raise Exception('Invalid name')