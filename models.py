#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode, force_unicode
from django import forms

from django.db.models.signals import post_save
from django.dispatch import receiver


class Masivo(models.Model):

    tipo = models.TextField(max_length=30, blank=True)
    cantidad = models.CharField(max_length=30, blank=True)
    documentos = models.CharField(max_length=30, blank=True)
    code_user = models.CharField(max_length=330, blank=True)
    codgrupo = models.CharField(max_length=20, blank=True)
    titulo = models.CharField(max_length=400)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_ingreso = models.DateField(auto_now_add=False)
    descripcion = models.CharField(max_length=400)
    cisco = models.CharField(max_length=400)
    tema = models.CharField(max_length=400)
    gestor = models.CharField(max_length=100)
    gestor_enc = models.CharField(max_length=100)
    flag = models.CharField(max_length=1, default=0)
    codu = models.CharField('Codu:', max_length=4)

    def __unicode__(self):
        return str(self.pk)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supervision = models.TextField(max_length=30, blank=True)
    grupo = models.CharField(max_length=30, blank=True)
    uuoo = models.CharField(max_length=30, blank=True)
    id_user = models.CharField(max_length=20, blank=True)
    codgrupo = models.CharField(max_length=20, blank=True)
    supervisor = models.CharField(max_length=200)
    nom_completo = models.CharField(max_length=400, blank=True)
    
    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class Llamada(models.Model):
    code = models.CharField(max_length=20)
    ruc = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=400)
    telefono = models.CharField(max_length=400)
    contacto = models.CharField(max_length=400)
    titulo = models.CharField(max_length=400)
    descripcion = models.CharField(max_length=400)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_ingreso = models.DateField(auto_now_add=False)
    hora = models.CharField(max_length=400)
    anexo = models.CharField(max_length=400)
    estado = models.CharField(max_length=400)
    grupo = models.CharField(max_length=400)
    cisco = models.CharField(max_length=400)
    tema = models.CharField(max_length=400)
    uuoo = models.CharField(max_length=400)
    adjunto = models.FileField(upload_to='reportes', blank=True, null=True)
    flag = models.CharField(max_length=1, default=0)
    gestor = models.CharField(max_length=400)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

class CierreLlamada(models.Model):
    llamada = models.ForeignKey(Llamada)
    code = models.CharField(max_length=20)
    user_id = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=400)
    respuesta = models.CharField(max_length=400)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_ingreso = models.DateField(auto_now_add=False)
    estado = models.CharField(max_length=400)
    hora = models.CharField(max_length=400)
    anexo = models.CharField(max_length=400)
    flag2 = models.CharField(max_length=1, default=0)
    gestor = models.CharField(max_length=400)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

class Volante(models.Model):
    registro = models.CharField(max_length=400)
    nombres = models.CharField(max_length=400)
    fecha_act = models.DateField(auto_now_add=False)
    hora_ini = models.CharField(max_length=400)
    hora_fin = models.CharField(max_length=400)
    usuario = models.CharField(max_length=400)
    host = models.CharField(max_length=400)
    anexo = models.CharField(max_length=400)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

class Gestor(models.Model):
    usuario = models.CharField(max_length=400)
    anexo = models.CharField(max_length=400)
    registro = models.CharField(max_length=400)
    fecha1 = models.DateField(auto_now_add=False)
    fecha2 = models.DateField(auto_now_add=False)
    fecha_reg = models.DateField(auto_now_add=True)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

class LlamadaLog(models.Model):
    code = models.CharField(max_length=20)
    id_llamada = models.CharField(max_length=50)
    id_adicional = models.CharField(max_length=50)
    user_id = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=400)
    telefono = models.CharField(max_length=400)
    contacto = models.CharField(max_length=400)
    titulo = models.CharField(max_length=400)
    descripcion = models.CharField(max_length=400)
    respuesta = models.CharField(max_length=400)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_ingreso = models.DateField(auto_now_add=False)
    hora = models.CharField(max_length=400)
    anexo = models.CharField(max_length=400)
    estado = models.CharField(max_length=400)
    grupo = models.CharField(max_length=400)
    cisco = models.CharField(max_length=400)
    tema = models.CharField(max_length=400)
    uuoo = models.CharField(max_length=400)
    adjunto = models.FileField(upload_to='reportes', blank=True, null=True)
    flag = models.CharField(max_length=1, default=0)
    flag2 = models.CharField(max_length=1, default=0)
    gestor = models.CharField(max_length=400)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

class ReporteTramite(models.Model):
    fecha = models.DateField(auto_now_add=False)
    hora_ini = models.CharField(max_length=10)
    hora_fin = models.CharField(max_length=10)
    gestor = models.CharField(max_length=400)
    registro = models.CharField(max_length=400)
    user_id = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=400)
    dependencia = models.CharField(max_length=200)
    lote = models.CharField(max_length=50)
    cir = models.CharField(max_length=50)
    hora_tot = models.CharField(max_length=10)
    correo = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=200)
    ficha_ruc = models.CharField(max_length=200)
    dice = models.CharField(max_length=400)
    debe_decir = models.CharField(max_length=400)
    dato1 = models.BooleanField(default=0, blank=True)
    dato2 = models.BooleanField(default=0, blank=True)
    dato3 = models.BooleanField(default=0, blank=True)
    dato4 = models.BooleanField(default=0, blank=True)
    dato5 = models.BooleanField(default=0, blank=True)
    dato6 = models.BooleanField(default=0, blank=True)
    dato7 = models.BooleanField(default=0, blank=True)
    dato8 = models.BooleanField(default=0, blank=True)
    dato9 = models.BooleanField(default=0, blank=True)
    dato10 = models.BooleanField(default=0, blank=True)
    dato11 = models.BooleanField(default=0, blank=True)
    obs = models.CharField(max_length=400)
    adjunto = models.FileField(upload_to='tramites', blank=True, null=True)
    respuesta = models.CharField(max_length=1000)
    fecha_reg = models.DateField(auto_now_add=True)
    flag21 = models.CharField(max_length=1, default=0)
    estado = models.CharField(max_length=15)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

class ReporteChat(models.Model):
    fecha = models.DateField(auto_now_add=False)
    registro = models.CharField(max_length=400)
    tipo_doc = models.CharField(max_length=400)
    user_id = models.CharField(max_length=11)
    consulta = models.CharField(max_length=400)
    tema = models.CharField(max_length=300)
    subtema = models.CharField(max_length=400)
    tema1 = models.CharField(max_length=300, blank=True, null=True)
    subtema1 = models.CharField(max_length=400, blank=True, null=True)
    tema2 = models.CharField(max_length=300, blank=True, null=True)
    subtema2 = models.CharField(max_length=400, blank=True, null=True)
    tema3 = models.CharField(max_length=300, blank=True, null=True)
    subtema3 = models.CharField(max_length=400, blank=True, null=True)
    correo = models.EmailField(max_length=254)
    hora_ini = models.TimeField(auto_now=False)
    hora_fin = models.TimeField(auto_now=False)
    hora_tot = models.TimeField(auto_now=False)
    contacto = models.CharField(max_length=400)
    observa = models.CharField(max_length=400)
    adjunto = models.FileField(upload_to='chat', blank=True, null=True)
    piloto = models.CharField(max_length=50)
    gestor = models.CharField(max_length=400)
    semana = models.CharField(max_length=50)
    mes = models.CharField(max_length=25)
    rango= models.CharField(max_length=25)
    cantidad = models.CharField(max_length=20)
    fecha_reg = models.DateField(auto_now_add=True)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

#CASOINICIAL
class RegistroCaso(models.Model):
    code = models.CharField(max_length=15)
    fecha_correo = models.DateField(auto_now_add=False)
    hora_correo = models.CharField(max_length=11)
    user_id = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=400)
    telefono = models.CharField(max_length=400)
    contacto = models.CharField(max_length=400)
    titulo = models.CharField(max_length=400)
    descripcion = models.CharField(max_length=1000)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_ingreso = models.DateField(auto_now_add=False)
    cisco = models.CharField(max_length=400)
    tema = models.CharField(max_length=400)
    adjunto = models.FileField(upload_to='casos', blank=True, null=True)
    flag21 = models.CharField(max_length=1, default=0)
    gestor_enc = models.CharField(max_length=100)
    fecha_asi = models.DateField(auto_now_add=False)
    fecha_cie = models.DateField(auto_now_add=False)
    sigesi = models.CharField(max_length=500)
    respuesta = models.CharField(max_length=1000)
    gestor = models.CharField(max_length=400)
    grupo = models.CharField(max_length=400)
    uuoo = models.CharField(max_length=400)
    codgrupo = models.CharField(max_length=20)
    estado  = models.CharField(max_length=250)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

#SEGUIMIENTOCASO
class AsignarCaso(models.Model):
    code = models.ForeignKey(RegistroCaso)
    gestor_enc = models.CharField(max_length=100)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_asi = models.DateField(auto_now_add=False, default=False)
    flag22 = models.CharField(max_length=1, default=0)
    gestor = models.CharField(max_length=400)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)

#CIERRECASO
class CierreCaso(models.Model):
    code = models.ForeignKey(RegistroCaso)
    gestor_enc = models.CharField(max_length=100)
    fecha_reg = models.DateField(auto_now_add=True)
    fecha_cie = models.DateField(auto_now_add=False, default=False)
    sigesi = models.CharField(max_length=500)
    respuesta = models.CharField(max_length=400)
    flag22 = models.CharField(max_length=1, default=0)
    gestor = models.CharField(max_length=400)
    adjunto = models.FileField(upload_to='pauta', blank=True, null=True)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)


class RespuestaTramite(models.Model):

    code = models.ForeignKey(ReporteTramite)
    respuesta = models.TextField(max_length=400, blank=True)
    adjunto = models.FileField(upload_to='pauta', blank=True, null=True)
    estado = models.CharField(max_length=15)
    flag22 = models.CharField(max_length=1, default=0)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)


#CASOINICIAL
class Consolidado(models.Model):
    code = models.CharField(max_length=15)
    fecha_consolidado = models.DateField(auto_now_add=False)
    supervisor = models.CharField(max_length=250)
    adjunto = models.FileField(upload_to='casos', blank=True, null=True)
    codu = models.CharField('Codu:', max_length=15)

    def __unicode__(self):
        return str(self.pk)
