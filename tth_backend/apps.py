from django.apps import AppConfig


class TthBackendConfig(AppConfig):
    name = 'tth_backend'

# Added here so that front-end doesn't have to worry about these 
class TthFrontendConfig(AppConfig):
    name = 'tth_frontend'
