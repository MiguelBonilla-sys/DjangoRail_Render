# blog/management/commands/setup_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from blog.Models.CursosModel import Cursos
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.ProyectosModel import Proyectos
from blog.Models.NoticiasModel import Noticias
from blog.Models.AuditLogModel import AuditLog
from blog.Models.ConferenciasModel import Conferencias
from blog.Models.OfertasEmpleoModel import OfertasEmpleo
class Command(BaseCommand):
    help = 'Setup groups and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        staff_group, created = Group.objects.get_or_create(name='Staff')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Assign permissions to the staff group
        models_to_assign = [Cursos, Integrantes, Noticias, Proyectos, AuditLog, Conferencias, OfertasEmpleo]
        for model in models_to_assign:
            content_type = ContentType.objects.get_for_model(model)
            for perm in Permission.objects.filter(content_type=content_type):
                if perm.codename.startswith(('add_', 'change_', 'delete_', 'view_')):
                    staff_group.permissions.add(perm)
                    admin_group.permissions.add(perm)

        # Assign all permissions to the admin group
        admin_group.permissions.set(Permission.objects.all())

        # Configure the periodic task to run daily
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Eliminar ofertas expiradas',
            task='blog.tasks.eliminar_ofertas_expiradas',
        )