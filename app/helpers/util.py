from app.models.settingsmodel import settings


def app_config():
    config = settings.query.first()

    return config
