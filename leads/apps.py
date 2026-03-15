from django.apps import AppConfig


class LeadsConfig(AppConfig):
    name = 'leads'

    def ready(self):
        # Yeh line signals ko register karti hai
        import leads.signals