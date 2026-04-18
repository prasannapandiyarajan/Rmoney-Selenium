from configparser import ConfigParser

config = ConfigParser()
config.read('rmoney.production.properties')


class Props:
    # <-------------------------------------------- MAIL TRIGGER ------------------------------------------------------>
    # MAIL_CREDENTIAL_HOST = config.get('MAIL_TRIGGER', 'mail_credential.host')
    MAIL_PORT = config.get('MAIL_TRIGGER', 'port.mail')
    MAIL_HOST = config.get('MAIL_TRIGGER', 'host.mail')
    MAIL_PASS = config.get('MAIL_TRIGGER', 'pass.mail')
    MAIL_SENDER = config.get('MAIL_TRIGGER', 'sender.mail')
    MAIL_API_URl = config.get('MAIL_TRIGGER', 'api_url.mail')
    MAIL_APP_KEY = config.get('MAIL_TRIGGER', 'app_key.mail')
    MAIL_RECEIVER = config.get('MAIL_TRIGGER', 'receiver.mail')
    MAIL_DEVELOPER = config.get('MAIL_TRIGGER', 'developer.mail')

    MAIL_TRY_AGAIN = config.get('MAIL_TRIGGER', 'try_Again.mail')
    MAIL_TRY_SLEEP_TIME_DELAY = config.get('MAIL_TRIGGER', 'try_sleep_time.mail')
