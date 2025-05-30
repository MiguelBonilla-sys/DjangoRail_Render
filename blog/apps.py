from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # Conectar la señal post_migrate para ejecutar código después de las migraciones
        post_migrate.connect(blog_callback, sender=self)

def blog_callback(sender, **kwargs):
    # Ejecutar el comando setup_groups después de las migraciones
    call_command('setup_groups')