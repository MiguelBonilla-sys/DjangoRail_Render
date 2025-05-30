from django.contrib import admin
from blog.Models.CursosModel import Cursos
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.ProyectosModel import Proyectos
from blog.Models.NoticiasModel import Noticias
from blog.Models.AuditLogModel import AuditLog
from blog.Models.ConferenciasModel import Conferencias
from blog.Models.OfertasEmpleoModel import OfertasEmpleo

# Registrar modelos para que aparezcan en el panel de administración
admin.site.register(AuditLog)
admin.site.register(Conferencias)
admin.site.register(Cursos)
admin.site.register(Noticias)
admin.site.register(Integrantes)
admin.site.register(Proyectos)
admin.site.register(OfertasEmpleo)