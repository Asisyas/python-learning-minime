import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def get_section( section ):
    return config[section]

def get_parameter( section, parameter ):
    sctn = get_section(section)

    if sctn is None:
        return None

    return sctn[parameter]