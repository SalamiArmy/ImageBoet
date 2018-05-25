import main
getgif = main.get_platform_command_code('web', 'getgif')
def run(keyConfig, message, totalResults=1):
    return getgif.run(keyConfig, message, totalResults)
