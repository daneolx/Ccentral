# -*- coding: utf-8 -*-
from principal.models import Profile, Llamada, User, Volante, Gestor, CierreLlamada, LlamadaLog, ReporteTramite, RespuestaTramite ,ReporteChat, RegistroCaso, AsignarCaso, CierreCaso, Masivo, Consolidado
from django.db import models
from principal.forms import ProfileForm, LlamadaForm, EditarContrasenaForm, VolanteForm, GestorForm, CierreLlamadaForm, LlamadaLogForm ,EditarTramiteForm,ReporteTramiteForm, RespuestaTramiteForm, MasivoForm,ReporteChatForm,RegistroCasoForm, AsignarCasoForm, CierreCasoForm, EditarCasoForm, EditarCasoIniForm, EditarLlamadaForm, EditarChatForm, EditarUserForm, ConsolidadoForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
import os
from sistema.settings import STATIC_URL, BASE_DIR, MEDIA_ROOT
from django.template.loader import render_to_string
import cStringIO as StringIO
import cgi
import mimetypes
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, date, time, timedelta
import sys
from django.contrib.auth.hashers import make_password
from .forms import (EditarContrasenaForm)
import djqscsv
from django.shortcuts import redirect
from djqscsv import render_to_csv_response
from django.utils import timezone
from django.utils.timesince import timesince
import calendar


@login_required
def cambiar_grupo(request, id):
    dato =get_object_or_404(Profile, id=id)
    if request.POST:
        formulario = EditarUserForm(request.POST, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect("/user_mante/")
    else:
        formulario = EditarUserForm(instance=dato)

    return render_to_response('cambiar_grupo.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))

@login_required
def search20(request):
    query = request.GET.get('q', '')
    if query:
        dato = RegistroCaso.objects.filter(Q(ruc__icontains=query)).order_by('-id')
    else:
        dato = []

    if query:
        llamadas = Llamada.objects.filter(Q(ruc__icontains=(query))).order_by('-id')
    else:
        llamadas = []

    return render_to_response("busqueda.html", {'time':datetime.now(),
        "dato": dato,
        "llamadas":llamadas
    }, context_instance=RequestContext(request))

@login_required
def search5(request):
    dato = RegistroCaso.objects.all().order_by('-id')
    query = request.GET.get('grupo', '')
    if query:
        dato = RegistroCaso.objects.filter(Q(cisco__icontains=query)).order_by('-id')
    else:
        dato = []
    return render_to_response("bandeja_asignados.html", {'time':datetime.now(),"query": query,'dato':dato}, context_instance=RequestContext(request))

#MASIVOS
@login_required
def bandeja_masivos(request):
    dato = Masivo.objects.order_by('-id')
    return render_to_response('bandeja_masivos.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))


@login_required
def registro_masivo(request):

    if request.method=='POST':
        formulario = MasivoForm(request.POST, request.FILES)
        Masivo(
            tipo = request.POST["tipo"],
            cantidad = request.POST["cantidad"],
            documentos = request.POST["documentos"],
            rucs = request.POST["rucs"],
            codgrupo = request.POST["codgrupo"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            gestor = request.POST["gestor"],
            codu = request.POST["codu"],
            flag = request.POST["flag"]
        ).save()
        return HttpResponseRedirect('/bandeja_masivos')
    else:
        formulario = MasivoForm()
    return render(request, "registro_masivo.html", {'time':datetime.now()})

#CASOS

@login_required(login_url='/ingresar')
def devolver_llamada(request, id):
    dato = RegistroCaso.objects.get(pk=id)
    conteo = Llamada.objects.count()

    if conteo == 0:
        conteo = 1
    else:
        conteo = Llamada.objects.count() + 1

    if request.method=='POST':
        formulario = LlamadaForm(request.POST, request.FILES)
        Llamada(
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            gestor = request.POST["gestor"],
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            flag = request.POST["flag"],
            code = request.POST["code"],
            codu = request.user
        ).save()
        LlamadaLog(
            id_llamada = request.POST["id_llamada"],
            id_adicional = request.POST["id_adicional"],
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            gestor = request.POST["gestor"],
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            flag = request.POST["flag"],
            code = request.POST["code"],
            codu = request.user
        ).save()
        return HttpResponseRedirect('/devoluciones')
    else:
        formulario = LlamadaForm()
    return render(request, "devolucion_llamadas2.html", {'conteo':conteo,'time':datetime.now(), 'dato':dato})

@login_required
def mis_casos(request):
    dato = RegistroCaso.objects.filter(codu=request.user).order_by('-id')

    from django.db import connection
    # Data modifying operation - commit required
    with connection.cursor() as cursor:
        cursor.execute("UPDATE principal_registrocaso SET code = (SELECT CONCAT((SELECT LEFT (code,7)),id));")
        cursor.execute("UPDATE principal_registrocaso SET adjunto='-' where adjunto='';")
        row = cursor.fetchone()

    return render_to_response('mis_casos.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def mis_asignados(request):
    dato = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).order_by('-id')
    return render_to_response('mis_asignados.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def casos_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).order_by('-id')
    return render_to_response('casos_grupo.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def pendientes_cierre(request):
    dato = RegistroCaso.objects.filter(flag21__in=['1']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_con_sigesi(request):
    dato = RegistroCaso.objects.filter(flag21__in=['3']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def bandeja_consolidado(request):
    dato = Consolidado.objects.all().order_by('-id')
    return render_to_response('bandeja_consolidado.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def registro_consolidado(request):

    if request.method=='POST':
        formulario = ConsolidadoForm(request.POST, request.FILES)
        Consolidado(
            code = request.POST["code"],
            fecha_consolidado = request.POST["fecha_consolidado"],
            supervisor = request.POST["supervisor"],
            adjunto = request.FILES.get('adjunto', '0'),
            codu = request.user
        ).save()
        return HttpResponseRedirect('/bandeja_consolidado')
    else:
        formulario = ConsolidadoForm()
    return render(request, "registro_consolidado.html", {'time':datetime.now()})

@login_required
def casos_ate_grupo(request):
    dato = RegistroCaso.objects.filter(flag21__in=['5']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_ate_sigesi(request):
    dato = RegistroCaso.objects.filter(flag21__in=['6']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_devuelto(request):
    dato = RegistroCaso.objects.filter(flag21__in=['7']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def concluidos(request):
    dato = RegistroCaso.objects.filter(flag21__in=['4']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_concluidos.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

#GRUPO

@login_required
def todos(request):
    dato = RegistroCaso.objects.order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def todos_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def pendientes_cierre_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['1']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_csigesi_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['3']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_ategrupo_sigesi(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['5']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_atesigesi_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['6']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def casos_devuelto_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['7']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def concluidos_grupo(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['4']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('todos_grupo.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def supervisores_casos(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Registrado' WHERE flag21 ='0';")
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Asignado' WHERE flag21 ='1';")
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Con SIGESI' WHERE flag21 ='3';")
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Cerrado' WHERE flag21 ='4';")
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Atendido por Grupo' WHERE flag21 ='5';")
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Atendido SIGESI' WHERE flag21 ='6';")
        cursor.execute("UPDATE principal_registrocaso SET estado = 'Devuelto' WHERE flag21 ='7';")
        row1=cursor.fetchone()

    dato = RegistroCaso.objects.all().order_by('-id')
    return render_to_response('supervisor_casos.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def bandeja_asignados(request):
    dato = RegistroCaso.objects.filter(flag21__in=['1', '2']).order_by('-id')
    dato2 = AsignarCaso.objects.filter(code_id=dato)
    return render_to_response('bandeja_asignados.html',{'time':datetime.now(),'dato':dato,'dato2':dato2}, context_instance=RequestContext(request))

@login_required
def detalle_caso(request, id):
    dato = get_object_or_404(RegistroCaso, id=id)
    dato2 = CierreCaso.objects.filter(code_id=dato)
    return render_to_response('detalle_caso.html',{'dato':dato,'dato2':dato2,'time':datetime.now() }, context_instance=RequestContext(request))

@login_required
def detalle_caso_ind(request, id):
    dato = get_object_or_404(RegistroCaso, id=id)
    dato2 = CierreCaso.objects.filter(code=dato)
    return render_to_response('detalle_caso_ind.html',{'dato':dato,'dato2':dato2,'time':datetime.now() }, context_instance=RequestContext(request))

@login_required
def detalle_caso_asignado(request, id):
    dato = get_object_or_404(RegistroCaso, id=id)
    dato2 = CierreCaso.objects.filter(code=dato)
    return render_to_response('detalle_caso_asignado.html',{'dato':dato,'dato2':dato2,'time':datetime.now() }, context_instance=RequestContext(request))

@login_required
def detalle_caso_grupo(request, id):
    dato = get_object_or_404(RegistroCaso, id=id)
    dato2 = CierreCaso.objects.filter(code=dato)
    return render_to_response('detalle_caso_grupo.html',{'dato':dato,'dato2':dato2,'time':datetime.now() }, context_instance=RequestContext(request))

@login_required
def editar_asigna(request, id):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')

    gestor1 = Profile.objects.filter(codgrupo='C01').order_by('nom_completo')
    gestor2 = Profile.objects.filter(codgrupo='C12').order_by('nom_completo')
    gestor3 = Profile.objects.filter(codgrupo='C02').order_by('nom_completo')
    gestor4 = Profile.objects.filter(codgrupo='C16').order_by('nom_completo')
    gestor5 = Profile.objects.filter(codgrupo='C06').order_by('nom_completo')
    gestor6 = Profile.objects.filter(codgrupo='C05').order_by('nom_completo')
    gestor7 = Profile.objects.filter(codgrupo='C11').order_by('nom_completo')
    gestor8 = Profile.objects.filter(codgrupo='C10').order_by('nom_completo')
    gestor9 = Profile.objects.filter(codgrupo='C03').order_by('nom_completo')
    gestora = Profile.objects.filter(codgrupo='C13').order_by('nom_completo')
    gestor11 = Profile.objects.filter(codgrupo='C14').order_by('nom_completo')
    gestor12 = Profile.objects.filter(codgrupo='C09').order_by('nom_completo')
    gestor13 = Profile.objects.filter(codgrupo='C08').order_by('nom_completo')
    gestor14 = Profile.objects.filter(codgrupo='C07').order_by('nom_completo')
    dato =get_object_or_404(RegistroCaso, pk=id)
    dato2 =get_object_or_404(AsignarCaso, code_id=id)
    if request.POST:
        formulario = EditarCasoForm(request.POST, instance=dato)
        if formulario.is_valid():
            formulario.save()
            dato2.flag22 = request.POST["flag22"]
            dato2.gestor_enc = request.POST["gestor_enc"]
            dato2.sigesi = request.POST["sigesi"]
            dato2.fecha_asi = request.POST["fecha_asi"]
            dato2.save()
        return HttpResponseRedirect("/casos_grupo/")
    else:
        formulario = EditarCasoForm(instance=dato)

    return render_to_response('editar_asigna.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato,'gestor14':gestor14,'gestor13':gestor13,'gestor12':gestor12,'gestor11':gestor11,'gestora':gestora,'gestor9':gestor9,'gestor8':gestor8,'gestor7':gestor7,'gestor6':gestor6,'gestor5':gestor5,'gestor':gestor,'gestor1':gestor1,'gestor2':gestor2,'gestor3':gestor3,'gestor4':gestor4}, context_instance=RequestContext(request))

@login_required
def editar_caso(request, id):
    dato =get_object_or_404(RegistroCaso, pk=id)
    if request.POST:
        formulario = EditarCasoIniForm(request.POST, request.FILES, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect("/mis_casos/")
    else:
        formulario = EditarCasoIniForm(instance=dato)

    return render_to_response('editar_caso.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))

@login_required
def cerrar_caso_fin(request, id):
    actu = RegistroCaso.objects.filter(pk=id).update(flag21='4')
    actu2 = CierreCaso.objects.filter(code=id).update(flag22='4')
    return HttpResponseRedirect("/mis_casos/")

@login_required
def cerrar_caso_sigesi(request, id):
    actu = RegistroCaso.objects.filter(pk=id).update(flag21='6')
    actu2 = CierreCaso.objects.filter(code=id).update(flag22='6')
    return HttpResponseRedirect("/mis_asignados/")

@login_required
def cerrar_caso(request, id):
    inci = RegistroCaso.objects.get(pk=id)
    if request.method=='POST':
        formulario = CierreCasoForm(request.POST, request.FILES)
        CierreCaso(
            code = inci,
            fecha_cie = request.POST["fecha_cie"],
            sigesi = request.POST["sigesi"],
            respuesta = request.POST["respuesta"],
            gestor = request.POST["gestor"],
            gestor_enc = request.POST["gestor_enc"],
            adjunto = request.FILES.get('adjunto', '0'),
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.fecha_cie = request.POST["fecha_cie"]
        inci.respuesta = request.POST["respuesta"]
        inci.gestor_enc = request.POST["gestor_enc"]
        inci.sigesi = request.POST["sigesi"]
        inci.save()
        return HttpResponseRedirect(reverse(detalle_caso, args=(inci.pk,)))
    else:
        formulario = CierreCasoForm()
    return render_to_response('cerrar_caso.html',{'formulario':formulario,'time':datetime.now(),'inci':inci}, context_instance=RequestContext(request))

@login_required
def cerrar_caso2(request, id):
    inci = RegistroCaso.objects.get(pk=id)
    if request.method=='POST':
        formulario = CierreCasoForm(request.POST, request.FILES)
        CierreCaso(
            code = inci,
            fecha_cie = request.POST["fecha_cie"],
            respuesta = request.POST["respuesta"],
            gestor = request.POST["gestor"],
            gestor_enc = request.POST["gestor_enc"],
            adjunto = request.FILES.get('adjunto', '0'),
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.fecha_cie = request.POST["fecha_cie"]
        inci.respuesta = request.POST["respuesta"]
        inci.gestor_enc = request.POST["gestor_enc"]
        inci.save()
        return HttpResponseRedirect(reverse(detalle_caso, args=(inci.pk,)))
    else:
        formulario = CierreCasoForm()
    return render_to_response('cerrar_caso2.html',{'formulario':formulario,'time':datetime.now(),'inci':inci}, context_instance=RequestContext(request))

@login_required
def cerrar_caso3(request, id):
    inci = RegistroCaso.objects.get(pk=id)
    if request.method=='POST':
        formulario = CierreCasoForm(request.POST, request.FILES)
        CierreCaso(
            code = inci,
            fecha_cie = request.POST["fecha_cie"],
            respuesta = request.POST["respuesta"],
            gestor = request.POST["gestor"],
            gestor_enc = request.POST["gestor_enc"],
            adjunto = request.FILES.get('adjunto', '0'),
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.fecha_cie = request.POST["fecha_cie"]
        inci.respuesta = request.POST["respuesta"]
        inci.save()
        return HttpResponseRedirect(reverse(detalle_caso, args=(inci.pk,)))
    else:
        formulario = CierreCasoForm()
    return render_to_response('cerrar_caso3.html',{'formulario':formulario,'time':datetime.now(),'inci':inci}, context_instance=RequestContext(request))

@login_required
def asignar_caso2(request, id):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')
    inci = RegistroCaso.objects.get(pk=id)
    if request.POST:
        formulario = AsignarCasoForm(request.POST)
        AsignarCaso(
            code = inci,
            gestor_enc = request.POST["gestor_enc"],
            fecha_asi = request.POST["fecha_asi"],
            gestor = request.POST["gestor"],
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.gestor_enc = request.POST["gestor_enc"]
        inci.fecha_asi = request.POST["fecha_asi"]
        inci.save()
        return HttpResponseRedirect('/bandeja_casos')
    else:
        formulario = AsignarCasoForm()
    return render_to_response('asignar_caso2.html',{'formulario':formulario, 'time':datetime.now(),'inci':inci,'gestor':gestor}, context_instance=RequestContext(request))

@login_required
def asignar_caso(request, id):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')

    gestor1 = Profile.objects.filter(codgrupo='C01').order_by('nom_completo')
    gestor2 = Profile.objects.filter(codgrupo='C12').order_by('nom_completo')
    gestor3 = Profile.objects.filter(codgrupo='C02').order_by('nom_completo')
    gestor4 = Profile.objects.filter(codgrupo='C16').order_by('nom_completo')
    gestor5 = Profile.objects.filter(codgrupo='C06').order_by('nom_completo')
    gestor6 = Profile.objects.filter(codgrupo='C05').order_by('nom_completo')
    gestor7 = Profile.objects.filter(codgrupo='C11').order_by('nom_completo')
    gestor8 = Profile.objects.filter(codgrupo='C10').order_by('nom_completo')
    gestor9 = Profile.objects.filter(codgrupo='C03').order_by('nom_completo')
    gestora = Profile.objects.filter(codgrupo='C13').order_by('nom_completo')
    gestor11 = Profile.objects.filter(codgrupo='C14').order_by('nom_completo')
    gestor12 = Profile.objects.filter(codgrupo='C09').order_by('nom_completo')
    gestor13 = Profile.objects.filter(codgrupo='C08').order_by('nom_completo')
    gestor14 = Profile.objects.filter(codgrupo='C07').order_by('nom_completo')
    inci = RegistroCaso.objects.get(pk=id)
    if request.POST:
        formulario = AsignarCasoForm(request.POST)
        AsignarCaso(
            code = inci,
            gestor_enc = request.POST["gestor_enc"],
            fecha_asi = request.POST["fecha_asi"],
            gestor = request.POST["gestor"],
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.gestor_enc = request.POST["gestor_enc"]
        inci.fecha_asi = request.POST["fecha_asi"]
        inci.save()
        return HttpResponseRedirect('/bandeja_casos')
    else:
        formulario = AsignarCasoForm()
    return render_to_response('asignar_caso.html',{'formulario':formulario, 'time':datetime.now(),'gestor14':gestor14,'gestor13':gestor13,'gestor12':gestor12,'gestor11':gestor11,'gestora':gestora,'gestor9':gestor9,'gestor8':gestor8,'gestor7':gestor7,'gestor6':gestor6,'gestor5':gestor5,'inci':inci,'gestor':gestor,'gestor1':gestor1,'gestor2':gestor2,'gestor3':gestor3,'gestor4':gestor4}, context_instance=RequestContext(request))

@login_required
def asignar_caso_grupo(request, id):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')

    gestor1 = Profile.objects.filter(codgrupo='C01').order_by('nom_completo')
    gestor2 = Profile.objects.filter(codgrupo='C12').order_by('nom_completo')
    gestor3 = Profile.objects.filter(codgrupo='C02').order_by('nom_completo')
    gestor4 = Profile.objects.filter(codgrupo='C16').order_by('nom_completo')
    gestor5 = Profile.objects.filter(codgrupo='C06').order_by('nom_completo')
    gestor6 = Profile.objects.filter(codgrupo='C05').order_by('nom_completo')
    gestor7 = Profile.objects.filter(codgrupo='C11').order_by('nom_completo')
    gestor8 = Profile.objects.filter(codgrupo='C10').order_by('nom_completo')
    gestor9 = Profile.objects.filter(codgrupo='C03').order_by('nom_completo')
    gestora = Profile.objects.filter(codgrupo='C13').order_by('nom_completo')
    gestor11 = Profile.objects.filter(codgrupo='C14').order_by('nom_completo')
    gestor12 = Profile.objects.filter(codgrupo='C09').order_by('nom_completo')
    gestor13 = Profile.objects.filter(codgrupo='C08').order_by('nom_completo')
    gestor14 = Profile.objects.filter(codgrupo='C07').order_by('nom_completo')
    inci = RegistroCaso.objects.get(pk=id)
    if request.POST:
        formulario = AsignarCasoForm(request.POST)
        AsignarCaso(
            code = inci,
            gestor_enc = request.POST["gestor_enc"],
            fecha_asi = request.POST["fecha_asi"],
            gestor = request.POST["gestor"],
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.gestor_enc = request.POST["gestor_enc"]
        inci.fecha_asi = request.POST["fecha_asi"]
        inci.save()
        return HttpResponseRedirect('/casos_grupo')
    else:
        formulario = AsignarCasoForm()
    return render_to_response('asignar_caso.html',{'formulario':formulario, 'time':datetime.now(),'gestor14':gestor14,'gestor13':gestor13,'gestor12':gestor12,'gestor11':gestor11,'gestora':gestora,'gestor9':gestor9,'gestor8':gestor8,'gestor7':gestor7,'gestor6':gestor6,'gestor5':gestor5,'inci':inci,'gestor':gestor,'gestor1':gestor1,'gestor2':gestor2,'gestor3':gestor3,'gestor4':gestor4}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def devolucionllamadas2(request):
    conteo = Llamada.objects.count()

    if conteo == 0:
        conteo = 1
    else:
        conteo = Llamada.objects.count() + 1

    if request.method=='POST':
        formulario = LlamadaForm(request.POST, request.FILES)
        Llamada(
            ruc = request.POST["ruc"],
            code = request.POST["code"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            gestor = request.user.get_full_name(),
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            flag = request.POST["flag"],
            codu = request.user
        ).save()
        LlamadaLog(
            id_llamada = request.POST["id_llamada"],
            code = request.POST["code"],
            id_adicional = request.POST["id_adicional"],
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            gestor = request.user.get_full_name(),
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            flag = request.POST["flag"],
            codu = request.user
        ).save()
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect('/devoluciones')
    else:
        formulario = LlamadaForm()
    return render(request, "devolucion_llamadas.html", {'conteo':conteo,'time':datetime.now()})

@login_required
def search3(request):
    minimo = datetime.strptime(request.GET['minimo'], '%Y-%m-%d')
    maximo = datetime.strptime(request.GET['maximo'], '%Y-%m-%d')

    if minimo and maximo:
        dato = RegistroCaso.objects.filter(Q(fecha_ingreso__range=(minimo,maximo))).order_by('-id')
    else:
        dato = []
    return render_to_response("bandeja_asignados.html", {'time':datetime.now(),
        "minimo": minimo,
        'maximo': maximo,
        "dato":dato
    }, context_instance=RequestContext(request))

@login_required
def bandeja_casos(request):
    dato = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21='0').order_by('-id')
    return render_to_response('bandeja_casos.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def registrar_caso(request):
    conteo = RegistroCaso.objects.count()

    if conteo == 0:
        conteo = 1
    else:
        conteo = RegistroCaso.objects.count() + 1

    if request.method=='POST':
        formulario = RegistroCasoForm(request.POST, request.FILES)
        RegistroCaso(
            code = request.POST["code"],
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            gestor = request.user.get_full_name(),
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            codgrupo = request.POST["codgrupo"],
            codu = request.user
        ).save()
        return HttpResponseRedirect('/mis_casos')
    else:
        formulario = RegistroCasoForm()
    return render(request, "registro_caso.html", {'conteo':conteo,'time':datetime.now()})

@login_required
def registrar_caso_pse(request):
    conteo = RegistroCaso.objects.count()

    if conteo == 0:
        conteo = 1
    else:
        conteo = RegistroCaso.objects.count() + 1

    if request.method=='POST':
        formulario = RegistroCasoForm(request.POST, request.FILES)
        RegistroCaso(
            code = request.POST["code"],
            ruc = request.POST["ruc"],
            fecha_correo = request.POST["fecha_correo"],
            hora_correo = request.POST["hora_correo"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            gestor = request.user.get_full_name(),
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            codgrupo = request.POST["codgrupo"],
            codu = request.user
        ).save()
        return HttpResponseRedirect('/mis_casos')
    else:
        formulario = RegistroCasoForm()
    return render(request, "registro_caso_pse.html", {'conteo':conteo,'time':datetime.now()})

#REPORTE SUPERVISOR

@login_required
def user_mante(request):
    usuario = User.objects.all().exclude(username='ADMIN')
    return render_to_response('usuarios.html',{'usuario':usuario}, context_instance=RequestContext(request))

@login_required
def reporte_sup(request):
    info = Llamada.objects.all()

    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()
    return render_to_response('reporte_sup.html',{'tot':tot,'info':info,'coe':coe,'sie':sie}, context_instance=RequestContext(request))

@login_required
def reporte_total(request):
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate = startdate - timedelta(days=1)
    enddate2 = startdate - timedelta(days=2)
    enddate3 = startdate - timedelta(days=3)

    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)

    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()
    
    #ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    #verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    #rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').count() 
    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').count() 

    treed = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').count()
    twod = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').count()
    oned = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    return render_to_response('reporte_total3.html',{'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def reporte_temas(request):
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate = startdate - timedelta(days=1)
    enddate2 = startdate - timedelta(days=2)
    enddate3 = startdate - timedelta(days=3)

    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)

    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()
    
    #ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    #verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    #rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').count() 
    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').count() 

    treed = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').count()
    twod = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').count()
    oned = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    return render_to_response('reporte_temas.html',{'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))


@login_required
def reporte_gestor(request):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate = startdate - timedelta(days=1)
    enddate2 = startdate - timedelta(days=2)
    enddate3 = startdate - timedelta(days=3)

    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)

    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()
    
    #ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    #verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    #rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').count() 
    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').count() 

    treed = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').count()
    twod = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').count()
    oned = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    return render_to_response('reporte_gestor.html',{'gestor':gestor,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def search_gestor(request):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')
    query = request.GET.get('gestor', '')

    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').filter(gestor=query).count()
    sie = Llamada.objects.filter(estado='Sin Éxito').filter(gestor=query).count()

    startdate = date.today()
    enddate = startdate - timedelta(days=1)
    enddate2 = startdate - timedelta(days=2)
    enddate3 = startdate - timedelta(days=3)

    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)

    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(gestor=query).count()
    
    #ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    #verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    #rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(gestor=query).count() 
    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(gestor=query).count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(gestor=query).count() 

    treed = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(gestor=query).count()
    twod = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(gestor=query).count()
    oned = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(gestor=query).count()

    pendi = RegistroCaso.objects.filter(flag21='3').filter(gestor=query).count()
    cerra = RegistroCaso.objects.filter(flag21='4').filter(gestor=query).count()

    return render_to_response('reporte_gestor.html',{'query':query,'gestor':gestor,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def search_tema(request):
    gestor = Profile.objects.filter(supervision='INFORMÁTICO').order_by('nom_completo')
    query = request.GET.get('tema', '')

    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').filter(tema=query).count()
    sie = Llamada.objects.filter(estado='Sin Éxito').filter(tema=query).count()

    startdate = date.today()
    enddate = startdate - timedelta(days=1)
    enddate2 = startdate - timedelta(days=2)
    enddate3 = startdate - timedelta(days=3)

    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)

    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(gestor=query).count()
    
    #ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    #verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    #rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(tema=query).count() 
    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(tema=query).count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(tema=query).count() 

    treed = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(tema=query).count()
    twod = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(tema=query).count()
    oned = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(tema=query).count()

    pendi = RegistroCaso.objects.filter(flag21='3').filter(tema=query).count()
    cerra = RegistroCaso.objects.filter(flag21='4').filter(tema=query).count()

    return render_to_response('reporte_temas.html',{'query':query,'gestor':gestor,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def reporte_grupos(request):
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)


    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()

    rojo1 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='T-REGISTRO').count()
    rojo2 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='PLAME').count()
    rojo3 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Essalud - ONP - SIS').count()
    rojo4 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Detracciones').count()
    rojo5 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    rojo6 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='RUC').count()
    rojo7 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='PDT - Declara Fácil').count()
    rojo8 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='PDB').count()
    rojo9 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='COA').count()
    rojo10 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Otros Temas').count()
    rojo11 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Valicentro').count()
    rojo12 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Extranet').count()
    rojo13 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    rojo14 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='SEE (Del Contribuyente)').count()
    rojo15 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='SEE (Portal)').count()
    rojo16 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    rojo17 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    rojo18 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    rojo19 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    rojo20 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Supervisor Edgar').count()
    rojo21 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='Supervisor Javier').count()
    rojo22 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate30,enddate16]).filter(flag21='3').filter(cisco='PSE').count()
    
    ambar1 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='T-REGISTRO').count()
    ambar2 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='PLAME').count()
    ambar3 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Essalud - ONP - SIS').count()
    ambar4 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Detracciones').count()
    ambar5 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    ambar6 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='RUC').count()
    ambar7 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='PDT - Declara Fácil').count()
    ambar8 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='PDB').count()
    ambar9 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='COA').count()
    ambar10 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Otros Temas').count()
    ambar11 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Valicentro').count()
    ambar12 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Extranet').count()
    ambar13 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    ambar14 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='SEE (Del Contribuyente)').count()
    ambar15 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='SEE (Portal)').count()
    ambar16 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    ambar17 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    ambar18 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    ambar19 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    ambar20 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Supervisor Edgar').count()
    ambar21 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='Supervisor Javier').count()
    ambar22 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate15,enddate6]).filter(flag21='3').filter(cisco='PSE').count()

    verde1 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='T-REGISTRO').count()
    verde2 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='PLAME').count()
    verde3 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Essalud - ONP - SIS').count()
    verde4 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Detracciones').count()
    verde5 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    verde6 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='RUC').count()
    verde7 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='PDT - Declara Fácil').count()
    verde8 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='PDB').count()
    verde9 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='COA').count()
    verde10 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Otros Temas').count()
    verde11 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Valicentro').count()
    verde12 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Extranet').count()
    verde13 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    verde14 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='SEE (Del Contribuyente)').count()
    verde15 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='SEE (Portal)').count()
    verde16 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    verde17 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    verde18 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    verde19 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    verde20 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Supervisor Edgar').count()
    verde21 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='Supervisor Javier').count()
    verde22 = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__range=[enddate5,today]).filter(flag21='3').filter(cisco='PSE').count()

    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    treed = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-3))).filter(flag21='4').count()
    twod = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-2))).filter(flag21='4').count()
    oned = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-1))).filter(flag21='4').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(ruc) from principal_registrocaso WHERE datediff(current_date,date(fecha_cie)) = '1' and flag21='4' and sigesi like 'h%';")
        row1=cursor.fetchone()

    return render_to_response('reporte_grupos.html',{
        'rojo1':rojo1,'rojo2':rojo2,'rojo3':rojo3,'rojo4':rojo4,'rojo5':rojo5,'rojo6':rojo6,'rojo7':rojo7,'rojo8':rojo8,'rojo9':rojo9,'rojo10':rojo10,'rojo11':rojo11,'rojo12':rojo12,'rojo13':rojo13,'rojo14':rojo14,'rojo15':rojo15,'rojo16':rojo16,'rojo17':rojo17,'rojo18':rojo18,'rojo19':rojo19,'rojo20':rojo20,'rojo21':rojo21,'rojo22':rojo22,
        'ambar1':ambar1,'ambar2':ambar2,'ambar3':ambar3,'ambar4':ambar4,'ambar5':ambar5,'ambar6':ambar6,'ambar7':ambar7,'ambar8':ambar8,'ambar9':ambar9,'ambar10':ambar10,'ambar11':ambar11,'ambar12':ambar12,'ambar13':ambar13,'ambar14':ambar14,'ambar15':ambar15,'ambar16':ambar16,'ambar17':ambar17,'ambar18':ambar18,'ambar19':ambar19,'ambar20':ambar20,'ambar21':ambar21,'ambar22':ambar22,
        'verde1':verde1,'verde2':verde2,'verde3':verde3,'verde4':verde4,'verde5':verde5,'verde6':verde6,'verde7':verde7,'verde8':verde8,'verde9':verde9,'verde10':verde10,'verde11':verde11,'verde12':verde12,'verde13':verde13,'verde14':verde14,'verde15':verde15,'verde16':verde16,'verde17':verde17,'verde18':verde18,'verde19':verde19,'verde20':verde20,'verde21':verde21,'verde22':verde22,
        'row1':row1,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def reporte_grupos1(request):
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)


    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()

    rojo1 = RegistroCaso.objects.filter(flag21='3').filter(cisco='T-REGISTRO').count()
    rojo2 = RegistroCaso.objects.filter(flag21='3').filter(cisco='PLAME').count()
    rojo3 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Essalud - ONP - SIS').count()
    rojo4 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Detracciones').count()
    rojo5 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    rojo6 = RegistroCaso.objects.filter(flag21='3').filter(cisco='RUC').count()
    rojo7 = RegistroCaso.objects.filter(flag21='3').filter(cisco='PDT - Declara Fácil').count()
    rojo8 = RegistroCaso.objects.filter(flag21='3').filter(cisco='PDB').count()
    rojo9 = RegistroCaso.objects.filter(flag21='3').filter(cisco='COA').count()
    rojo10 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Otros Temas').count()
    rojo11 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Valicentro').count()
    rojo12 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Extranet').count()
    rojo13 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    rojo14 = RegistroCaso.objects.filter(flag21='3').filter(cisco='SEE (Del Contribuyente)').count()
    rojo15 = RegistroCaso.objects.filter(flag21='3').filter(cisco='SEE (Portal)').count()
    rojo16 = RegistroCaso.objects.filter(flag21='3').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    rojo17 = RegistroCaso.objects.filter(flag21='3').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    rojo18 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    rojo19 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    rojo20 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Supervisor Edgar').count()
    rojo21 = RegistroCaso.objects.filter(flag21='3').filter(cisco='Supervisor Javier').count()
    rojo22 = RegistroCaso.objects.filter(flag21='3').filter(cisco='PSE').count()
    
    ambar1 = RegistroCaso.objects.filter(flag21='4').filter(cisco='T-REGISTRO').count()
    ambar2 = RegistroCaso.objects.filter(flag21='4').filter(cisco='PLAME').count()
    ambar3 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Essalud - ONP - SIS').count()
    ambar4 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Detracciones').count()
    ambar5 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    ambar6 = RegistroCaso.objects.filter(flag21='4').filter(cisco='RUC').count()
    ambar7 = RegistroCaso.objects.filter(flag21='4').filter(cisco='PDT - Declara Fácil').count()
    ambar8 = RegistroCaso.objects.filter(flag21='4').filter(cisco='PDB').count()
    ambar9 = RegistroCaso.objects.filter(flag21='4').filter(cisco='COA').count()
    ambar10 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Otros Temas').count()
    ambar11 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Valicentro').count()
    ambar12 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Extranet').count()
    ambar13 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    ambar14 = RegistroCaso.objects.filter(flag21='4').filter(cisco='SEE (Del Contribuyente)').count()
    ambar15 = RegistroCaso.objects.filter(flag21='4').filter(cisco='SEE (Portal)').count()
    ambar16 = RegistroCaso.objects.filter(flag21='4').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    ambar17 = RegistroCaso.objects.filter(flag21='4').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    ambar18 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    ambar19 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    ambar20 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Supervisor Edgar').count()
    ambar21 = RegistroCaso.objects.filter(flag21='4').filter(cisco='Supervisor Javier').count()
    ambar22 = RegistroCaso.objects.filter(flag21='4').filter(cisco='PSE').count()

    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    treed = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-3))).filter(flag21='4').count()
    twod = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-2))).filter(flag21='4').count()
    oned = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-1))).filter(flag21='4').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(ruc) from principal_registrocaso WHERE datediff(current_date,date(fecha_cie)) = '1' and flag21='4' and sigesi like 'h%';")
        row1=cursor.fetchone()

    return render_to_response('reporte_grupos1.html',{
        'rojo1':rojo1,'rojo2':rojo2,'rojo3':rojo3,'rojo4':rojo4,'rojo5':rojo5,'rojo6':rojo6,'rojo7':rojo7,'rojo8':rojo8,'rojo9':rojo9,'rojo10':rojo10,'rojo11':rojo11,'rojo12':rojo12,'rojo13':rojo13,'rojo14':rojo14,'rojo15':rojo15,'rojo16':rojo16,'rojo17':rojo17,'rojo18':rojo18,'rojo19':rojo19,'rojo20':rojo20,'rojo21':rojo21,'rojo22':rojo22,
        'ambar1':ambar1,'ambar2':ambar2,'ambar3':ambar3,'ambar4':ambar4,'ambar5':ambar5,'ambar6':ambar6,'ambar7':ambar7,'ambar8':ambar8,'ambar9':ambar9,'ambar10':ambar10,'ambar11':ambar11,'ambar12':ambar12,'ambar13':ambar13,'ambar14':ambar14,'ambar15':ambar15,'ambar16':ambar16,'ambar17':ambar17,'ambar18':ambar18,'ambar19':ambar19,'ambar20':ambar20,'ambar21':ambar21,'ambar22':ambar22,
        'row1':row1,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def reporte_grupos2(request):
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate = startdate - timedelta(days=1)
    enddate2 = startdate - timedelta(days=2)
    enddate3 = startdate - timedelta(days=3)

    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)

    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()

    rojo1 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='T-REGISTRO').count()
    rojo2 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='PLAME').count()
    rojo3 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Essalud - ONP - SIS').count()
    rojo4 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Detracciones').count()
    rojo5 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    rojo6 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='RUC').count()
    rojo7 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='PDT - Declara Fácil').count()
    rojo8 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='PDB').count()
    rojo9 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='COA').count()
    rojo10 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Otros Temas').count()
    rojo11 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Valicentro').count()
    rojo12 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Extranet').count()
    rojo13 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    rojo14 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='SEE (Del Contribuyente)').count()
    rojo15 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='SEE (Portal)').count()
    rojo16 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    rojo17 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    rojo18 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    rojo19 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    rojo20 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Supervisor Edgar').count()
    rojo21 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='Supervisor Javier').count()
    rojo22 = RegistroCaso.objects.filter(fecha_asi__range=[enddate3,enddate3]).filter(flag21='1').filter(cisco='PSE').count()
    
    ambar1 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='T-REGISTRO').count()
    ambar2 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='PLAME').count()
    ambar3 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Essalud - ONP - SIS').count()
    ambar4 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Detracciones').count()
    ambar5 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    ambar6 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='RUC').count()
    ambar7 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='PDT - Declara Fácil').count()
    ambar8 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='PDB').count()
    ambar9 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='COA').count()
    ambar10 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Otros Temas').count()
    ambar11 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Valicentro').count()
    ambar12 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Extranet').count()
    ambar13 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    ambar14 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='SEE (Del Contribuyente)').count()
    ambar15 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='SEE (Portal)').count()
    ambar16 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    ambar17 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    ambar18 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    ambar19 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    ambar20 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Supervisor Edgar').count()
    ambar21 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='Supervisor Javier').count()
    ambar22 = RegistroCaso.objects.filter(fecha_asi__range=[enddate2,enddate2]).filter(flag21='1').filter(flag21='3').filter(cisco='PSE').count()

    verde1 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='T-REGISTRO').count()
    verde2 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='PLAME').count()
    verde3 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Essalud - ONP - SIS').count()
    verde4 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Detracciones').count()
    verde5 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    verde6 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='RUC').count()
    verde7 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='PDT - Declara Fácil').count()
    verde8 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='PDB').count()
    verde9 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='COA').count()
    verde10 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Otros Temas').count()
    verde11 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Valicentro').count()
    verde12 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Extranet').count()
    verde13 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    verde14 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='SEE (Del Contribuyente)').count()
    verde15 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='SEE (Portal)').count()
    verde16 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    verde17 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    verde18 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    verde19 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    verde20 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Supervisor Edgar').count()
    verde21 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='Supervisor Javier').count()
    verde22 = RegistroCaso.objects.filter(fecha_asi__range=[enddate,today]).filter(flag21='1').filter(cisco='PSE').count()

    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    treed = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-3))).filter(flag21='4').count()
    twod = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-2))).filter(flag21='4').count()
    oned = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-1))).filter(flag21='4').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(ruc) from principal_registrocaso WHERE datediff(current_date,date(fecha_cie)) = '1' and flag21='4' and sigesi like 'h%';")
        row1=cursor.fetchone()

    return render_to_response('reporte_grupos2.html',{
        'rojo1':rojo1,'rojo2':rojo2,'rojo3':rojo3,'rojo4':rojo4,'rojo5':rojo5,'rojo6':rojo6,'rojo7':rojo7,'rojo8':rojo8,'rojo9':rojo9,'rojo10':rojo10,'rojo11':rojo11,'rojo12':rojo12,'rojo13':rojo13,'rojo14':rojo14,'rojo15':rojo15,'rojo16':rojo16,'rojo17':rojo17,'rojo18':rojo18,'rojo19':rojo19,'rojo20':rojo20,'rojo21':rojo21,'rojo22':rojo22,
        'ambar1':ambar1,'ambar2':ambar2,'ambar3':ambar3,'ambar4':ambar4,'ambar5':ambar5,'ambar6':ambar6,'ambar7':ambar7,'ambar8':ambar8,'ambar9':ambar9,'ambar10':ambar10,'ambar11':ambar11,'ambar12':ambar12,'ambar13':ambar13,'ambar14':ambar14,'ambar15':ambar15,'ambar16':ambar16,'ambar17':ambar17,'ambar18':ambar18,'ambar19':ambar19,'ambar20':ambar20,'ambar21':ambar21,'ambar22':ambar22,
        'verde1':verde1,'verde2':verde2,'verde3':verde3,'verde4':verde4,'verde5':verde5,'verde6':verde6,'verde7':verde7,'verde8':verde8,'verde9':verde9,'verde10':verde10,'verde11':verde11,'verde12':verde12,'verde13':verde13,'verde14':verde14,'verde15':verde15,'verde16':verde16,'verde17':verde17,'verde18':verde18,'verde19':verde19,'verde20':verde20,'verde21':verde21,'verde22':verde22,
        'row1':row1,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def reporte_grupos3(request):
    info = Llamada.objects.all()
    today = date.today()
    #asignadas = int(Saldo1.objects.values('saldo_gal').last()["saldo_gal"]) - dscto1r
    tot = Llamada.objects.count()
    coe = Llamada.objects.filter(estado='Con Éxito').count()
    sie = Llamada.objects.filter(estado='Sin Éxito').count()

    startdate = date.today()
    enddate5 = startdate - timedelta(days=5)
    enddate6 = startdate - timedelta(days=6)
    enddate15 = startdate - timedelta(days=15)
    enddate16 = startdate - timedelta(days=16)
    enddate30 = startdate - timedelta(days=30)


    tot_sigesi = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).count()

    rojo1 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='T-REGISTRO').count()
    rojo2 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='PLAME').count()
    rojo3 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Essalud - ONP - SIS').count()
    rojo4 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Detracciones').count()
    rojo5 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    rojo6 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='RUC').count()
    rojo7 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='PDT - Declara Fácil').count()
    rojo8 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='PDB').count()
    rojo9 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='COA').count()
    rojo10 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Otros Temas').count()
    rojo11 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Valicentro').count()
    rojo12 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Extranet').count()
    rojo13 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    rojo14 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='SEE (Del Contribuyente)').count()
    rojo15 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='SEE (Portal)').count()
    rojo16 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    rojo17 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    rojo18 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    rojo19 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    rojo20 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Supervisor Edgar').count()
    rojo21 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='Supervisor Javier').count()
    rojo22 = Llamada.objects.filter(estado='Sin Éxito').filter(cisco='PSE').count()
    
    verde1 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='T-REGISTRO').count()
    verde2 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='PLAME').count()
    verde3 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Essalud - ONP - SIS').count()
    verde4 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Detracciones').count()
    verde5 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas').count()
    verde6 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='RUC').count()
    verde7 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='PDT - Declara Fácil').count()
    verde8 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='PDB').count()
    verde9 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='COA').count()
    verde10 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Otros Temas').count()
    verde11 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Valicentro').count()
    verde12 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Extranet').count()
    verde13 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Nuevo SEMT - Retención con terceros').count()
    verde14 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='SEE (Del Contribuyente)').count()
    verde15 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='SEE (Portal)').count()
    verde16 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='SLE - Sistema de Libro Electrónicos').count()
    verde17 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados').count()
    verde18 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta').count()
    verde19 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Centrales de Riesgo / Requerimientos de Pago').count()
    verde20 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Supervisor Edgar').count()
    verde21 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='Supervisor Javier').count()
    verde22 = Llamada.objects.filter(estado='Con Éxito').filter(cisco='PSE').count()

    ambar = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=15)).filter(flag21='4').count() 
    verde = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=5)).filter(flag21='4').count()
    rojo = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=30)).filter(flag21='4').count() 

    treed = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-3))).filter(flag21='4').count()
    twod = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-2))).filter(flag21='4').count()
    oned = RegistroCaso.objects.exclude(Q(sigesi__isnull=True) | Q(sigesi__exact='')).filter(fecha_cie__gt=datetime.now() - timedelta(days=(today.isoweekday()-1))).filter(flag21='4').count()

    pendi = RegistroCaso.objects.filter(flag21='3').count()
    cerra = RegistroCaso.objects.filter(flag21='4').count()

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(ruc) from principal_registrocaso WHERE datediff(current_date,date(fecha_cie)) = '1' and flag21='4' and sigesi like 'h%';")
        row1=cursor.fetchone()

    return render_to_response('reporte_grupos3.html',{
        'rojo1':rojo1,'rojo2':rojo2,'rojo3':rojo3,'rojo4':rojo4,'rojo5':rojo5,'rojo6':rojo6,'rojo7':rojo7,'rojo8':rojo8,'rojo9':rojo9,'rojo10':rojo10,'rojo11':rojo11,'rojo12':rojo12,'rojo13':rojo13,'rojo14':rojo14,'rojo15':rojo15,'rojo16':rojo16,'rojo17':rojo17,'rojo18':rojo18,'rojo19':rojo19,'rojo20':rojo20,'rojo21':rojo21,'rojo22':rojo22,
        'verde1':verde1,'verde2':verde2,'verde3':verde3,'verde4':verde4,'verde5':verde5,'verde6':verde6,'verde7':verde7,'verde8':verde8,'verde9':verde9,'verde10':verde10,'verde11':verde11,'verde12':verde12,'verde13':verde13,'verde14':verde14,'verde15':verde15,'verde16':verde16,'verde17':verde17,'verde18':verde18,'verde19':verde19,'verde20':verde20,'verde21':verde21,'verde22':verde22,
        'row1':row1,'oned':oned,'treed':treed,'twod':twod,'tot':tot,'info':info,'coe':coe,'sie':sie,'rojo':rojo,'ambar':ambar,'verde':verde,'tot_sigesi':tot_sigesi,'pendi':pendi,'cerra':cerra}, context_instance=RequestContext(request))

@login_required
def bandeja_tramite(request):
    dato = ReporteTramite.objects.all().order_by('-id')
    return render_to_response('bandeja_tramite.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def detalle_tramite(request, id):
    dato = get_object_or_404(ReporteTramite, id=id)
    dato2 = RespuestaTramite.objects.filter(code_id=dato)
    return render_to_response('detalle_tramite.html',{'dato':dato,'dato2':dato2,'time':datetime.now() }, context_instance=RequestContext(request))

@login_required
def registro_tramite(request):
    N = 14
    atras = datetime.now() - timedelta(days=N)
    adelante = datetime.now()
    if request.method=='POST':
        formulario = ReporteTramiteForm(request.POST, request.FILES)
        ReporteTramite(
            fecha = request.POST["fecha"],
            hora_ini = request.POST["hora_ini"],
            hora_fin = request.POST["hora_fin"],
            hora_tot = request.POST["hora_tot"],
            correo = request.POST["correo"],
            supervisor = request.POST["supervisor"],
            dice = request.POST["dice"],
            debe_decir = request.POST["debe_decir"],
            gestor = request.POST["gestor"],
            registro = request.POST["registro"],
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            dependencia = request.POST["dependencia"],
            lote = request.POST["lote"],
            cir = request.POST["cir"],
            dato1 = request.POST.get('dato1', ""),
            dato2 = request.POST.get('dato2', ""),
            dato3 = request.POST.get('dato3', ""),
            dato4 = request.POST.get('dato4', ""),
            dato5 = request.POST.get('dato5', ""),
            dato6 = request.POST.get('dato6', ""),
            dato7 = request.POST.get('dato7', ""),
            dato8 = request.POST.get('dato8', ""),
            dato9 = request.POST.get('dato9', ""),
            dato10 = request.POST.get('dato10', ""),
            dato11 = request.POST.get('dato11', ""),
            adjunto = request.FILES.get('adjunto', '0'),
            obs = request.POST["obs"],
            flag21 = request.POST["flag21"],
            codu = request.user
        ).save()
        return HttpResponseRedirect('/bandeja_tramite')
    else:
        formulario = ReporteTramiteForm()
    return render_to_response('registro_tramites.html',{'time':datetime.now(),'formulario':formulario,'atras':atras,'adelante':adelante}, context_instance=RequestContext(request))

@login_required
def cerrar_tramite(request, id):
    inci = ReporteTramite.objects.get(pk=id)
    if request.method=='POST':
        formulario = RespuestaTramiteForm(request.POST, request.FILES)
        RespuestaTramite(
            code = inci,
            respuesta = request.POST["respuesta"],
            adjunto = request.FILES.get('adjunto', '0'),
            estado = request.POST["estado"],
            flag22 = request.POST["flag22"],
            codu = request.POST["codu"]
        ).save()
        inci.flag21 = request.POST["flag21"]
        inci.respuesta = request.POST["respuesta"]
        inci.save()
        return HttpResponseRedirect(reverse(detalle_tramite, args=(inci.pk,)))
    else:
        formulario = RespuestaTramite()
    return render_to_response('cerrar_tramite.html',{'formulario':formulario,'time':datetime.now(),'inci':inci}, context_instance=RequestContext(request))

@login_required
def editar_tramite(request, id):
    dato =get_object_or_404(ReporteTramite, id=id)
    if request.POST:
        formulario = ReporteTramiteForm(request.POST, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect("/bandeja_tramite/")
    else:
        formulario = ReporteTramiteForm(instance=dato)

    return render_to_response('editar_tramite.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))

@login_required
def bandeja_chat(request):
    today =  datetime.now()
    conteo = ReporteChat.objects.filter(fecha_reg=today).filter(codu=request.user).count()
    conteo2 = ReporteChat.objects.filter(codu=request.user).count() + 1
    dato = ReporteChat.objects.all().order_by('-id')[0:1000]
    return render_to_response('bandeja_chat.html',{'time':datetime.now(),'dato':dato, 'today':today,'conteo':conteo,'conteo2':conteo2}, context_instance=RequestContext(request))

@login_required
def bandeja_chat_sup(request):
    today =  datetime.now()
    dato = ReporteChat.objects.all().order_by('-id')[0:1000]
    return render_to_response('bandeja_chat_sup.html',{'time':datetime.now(),'dato':dato, 'today':today}, context_instance=RequestContext(request))

@login_required
def eliminar_chat(request, id):
    dato = ReporteChat.objects.filter(pk=id).delete()
    return HttpResponseRedirect("/bandeja_chat_sup/")

@login_required
def registro_chat(request):
    N = 14

    atras = datetime.now() - timedelta(days=N)
    adelante = datetime.now()
    weekNumber = date.today().isocalendar()[1]

    #conteo = ReporteChat.objects.filter(fecha_reg=adelante).filter(codu=request.username).count()

    if request.method=='POST':
        formulario = ReporteChatForm(request.POST, request.FILES)
        ReporteChat(
            fecha = request.POST["fecha"],
            registro = request.POST["registro"],
            ruc = request.POST["ruc"],
            consulta = request.POST["consulta"],
            tema = request.POST["tema"],
            subtema = request.POST["subtema"],
            tipo_doc = request.POST["tipo_doc"],
            correo = request.POST["correo"],
            hora_ini = request.POST["hora_ini"],
            hora_fin = request.POST["hora_fin"],
            hora_tot = request.POST["hora_tot"],
            contacto = request.POST["contacto"],
            observa = request.POST.get("observa","-"),
            piloto = request.POST["piloto"],
            rango = request.POST["rango"],
            cantidad = request.POST["cantidad"],
            gestor = request.POST["gestor"],
            semana = request.POST["semana"],
            mes = request.POST["mes"],
            adjunto = request.FILES.get('adjunto', '-'),
            tema1 = request.POST.get("tema1","-"),
            subtema1 = request.POST.get("subtema1","-"),
            tema2 = request.POST.get("tema2","-"),
            subtema2 = request.POST.get("subtema2","-"),
            tema3 = request.POST.get("tema3","-"),
            subtema3 = request.POST.get("subtema3","-"),
            codu = request.user
        ).save()
        return HttpResponseRedirect('/bandeja_chat')
    else:
        formulario = ReporteChatForm()
    return render_to_response('registro_chat.html',{'time':datetime.now(),'formulario':formulario,'weekNumber':weekNumber,'atras':atras,'adelante':adelante}, context_instance=RequestContext(request))

@login_required
def registro_chat2(request):
    N = 14

    atras = datetime.now() - timedelta(days=N)
    adelante = datetime.now()
    weekNumber = date.today().isocalendar()[1]

    #conteo = ReporteChat.objects.filter(fecha_reg=adelante).filter(codu=request.username).count()

    if request.method=='POST':
        formulario = ReporteChatForm(request.POST, request.FILES)
        ReporteChat(
            fecha = request.POST["fecha"],
            registro = request.POST["registro"],
            ruc = request.POST["ruc"],
            consulta = request.POST["consulta"],
            tema = request.POST["tema"],
            subtema = request.POST["subtema"],
            tipo_doc = request.POST["tipo_doc"],
            correo = request.POST["correo"],
            hora_ini = request.POST["hora_ini"],
            hora_fin = request.POST["hora_fin"],
            hora_tot = request.POST["hora_tot"],
            contacto = request.POST["contacto"],
            observa = request.POST.get("observa","-"),
            piloto = request.POST["piloto"],
            rango = request.POST["rango"],
            cantidad = request.POST["cantidad"],
            gestor = request.POST["gestor"],
            semana = request.POST["semana"],
            mes = request.POST["mes"],
            adjunto = request.FILES.get('adjunto', '-'),
            tema1 = request.POST.get("tema1","-"),
            subtema1 = request.POST.get("subtema1","-"),
            tema2 = request.POST.get("tema2","-"),
            subtema2 = request.POST.get("subtema2","-"),
            tema3 = request.POST.get("tema3","-"),
            subtema3 = request.POST.get("subtema3","-"),
            codu = request.user
        ).save()
        return HttpResponseRedirect('/bandeja_chat')
    else:
        formulario = ReporteChatForm()
    return render_to_response('registro_chat3.html',{'time':datetime.now(),'formulario':formulario,'weekNumber':weekNumber,'atras':atras,'adelante':adelante}, context_instance=RequestContext(request))

@login_required
def editar_chat(request, id):
    dato =get_object_or_404(ReporteChat, id=id)
    if request.POST:
        formulario = EditarChatForm(request.POST, request.FILES, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect("/bandeja_chat/")
    else:
        formulario = EditarChatForm(instance=dato)

    from django.db import connection
    # Data modifying operation - commit required
    with connection.cursor() as cursor:
        cursor.execute("UPDATE principal_reportechat SET observa = '-' where observa = '';")
        row = cursor.fetchone()

    return render_to_response('editar_chat.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))

@login_required
def search2(request):
    minimo = datetime.strptime(request.GET['minimo'], '%Y-%m-%d')
    maximo = datetime.strptime(request.GET['maximo'], '%Y-%m-%d')

    if minimo and maximo:
        llamadas = Llamada.objects.filter(Q(fecha_ingreso__range=(minimo,maximo))).order_by('-id')
    else:
        llamadas = []
    return render_to_response("supervisores.html", {'time':datetime.now(),
        "minimo": minimo,
        'maximo': maximo,
        "llamadas":llamadas
    }, context_instance=RequestContext(request))

@login_required
def searchchat(request):
    minimo = datetime.strptime(request.GET['minimo'], '%Y-%m-%d')
    maximo = datetime.strptime(request.GET['maximo'], '%Y-%m-%d')

    if minimo and maximo:
        dato = ReporteChat.objects.filter(Q(fecha__range=(minimo,maximo))).order_by('-id')
    else:
        dato = []
    return render_to_response("bandeja_chat.html", {'time':datetime.now(),
        "minimo": minimo,
        'maximo': maximo,
        "dato":dato
    }, context_instance=RequestContext(request))

@login_required
def searchchat_sup(request):
    minimo = datetime.strptime(request.GET['minimo'], '%Y-%m-%d')
    maximo = datetime.strptime(request.GET['maximo'], '%Y-%m-%d')

    if minimo and maximo:
        dato = ReporteChat.objects.filter(Q(fecha__range=(minimo,maximo))).order_by('-id')
    else:
        dato = []

    return render_to_response("bandeja_chat_sup.html", {'time':datetime.now(),
        "minimo": minimo,
        'maximo': maximo,
        "dato":dato
    }, context_instance=RequestContext(request))

@login_required
def search4(request):
    minimo = datetime.strptime(request.GET['minimo'], '%Y-%m-%d')
    maximo = datetime.strptime(request.GET['maximo'], '%Y-%m-%d')

    if minimo and maximo:
        llamadas = Llamada.objects.filter(Q(fecha_ingreso__range=(minimo,maximo))).order_by('-id')
    else:
        llamadas = []
    return render_to_response("devoluciones.html", {'time':datetime.now(),
        "minimo": minimo,
        'maximo': maximo,
        "llamadas":llamadas
    }, context_instance=RequestContext(request))

@login_required
def buscar_volantes(request):
    dato = Volante.objects.all().order_by('-id')
    query = request.GET.get('q', '')
    if query:
        dato = Volante.objects.filter(
            Q(registro__icontains=query) | Q(nombres__icontains=query) | Q(usuario__icontains=query) |
            Q(anexo__icontains=query)).order_by('-id')
    else:
        dato = []
    return render_to_response("supervisor_volantes.html", {'time':datetime.now(),"query": query,'dato':dato}, context_instance=RequestContext(request))

@login_required
def buscar_usuarios(request):
    usuario = User.objects.all().order_by('-id')
    query = request.GET.get('q', '')
    if query:
        usuario = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)).order_by('-id')
    else:
        usuario = []
    return render_to_response("usuarios.html", {'time':datetime.now(),"query": query,'usuario':usuario}, context_instance=RequestContext(request))

@login_required
def registro_volantes(request):
    if request.method=='POST':
        formulario = VolanteForm(request.POST)
        Volante(
            registro = request.POST["registro"],
            nombres = request.POST["nombres"],
            fecha_act = request.POST["fecha_act"],
            hora_ini = request.POST["hora_ini"],
            hora_fin = request.POST["hora_fin"],
            usuario = request.POST["usuario"],
            anexo = request.POST["anexo"],
            codu = request.user
        ).save()
        return HttpResponseRedirect('/volantes')
    else:
        formulario = VolanteForm()
    return render_to_response('registro_volantes.html',{'time':datetime.now(),'formulario':formulario}, context_instance=RequestContext(request))

@login_required
def editar_volantes(request, id):
    dato =get_object_or_404(Volante, id=id)
    if request.POST:
        formulario = VolanteForm(request.POST, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect("/volantes/")
    else:
        formulario = VolanteForm(instance=dato)

    return render_to_response('editar_volantes.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))

@login_required
def editar_reiterativo(request, id):
    dato =get_object_or_404(CierreLlamada, id=id)
    if request.POST:
        formulario = CierreLlamadaForm(request.POST, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect(reverse(detalle, args=(dato.llamada,)))
    else:
        formulario = CierreLlamadaForm(instance=dato)

    return render_to_response('editar_reiterativo.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))

@login_required
def editar_devolucion(request, id):
    dato =get_object_or_404(Llamada, id=id)
    if request.POST:
        formulario = EditarLlamadaForm(request.POST, request.FILES, instance=dato)
        if formulario.is_valid():
            formulario.save()
        return HttpResponseRedirect(reverse(detalle, args=(dato.pk,)))
        #return HttpResponseRedirect("/devoluciones/")
    else:
        formulario = EditarLlamadaForm(instance=dato)

    return render_to_response('editar_llamada.html',{'time':datetime.now(),'formulario':formulario, 'dato':dato}, context_instance=RequestContext(request))


@login_required
def supervisor_volantes(request):
    dato = Volante.objects.all().order_by('-id')
    return render_to_response('supervisor_volantes.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def gestor_volantes(request):
    dato = Gestor.objects.all().order_by('-id')
    return render_to_response('gestor.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required
def supervisores_devolucion(request):
    llamadas = Llamada.objects.all().order_by('-id')
    return render_to_response('supervisores.html',{'time':datetime.now(),'llamadas':llamadas}, context_instance=RequestContext(request))

@login_required
def reportes_sup(request):
    llamadas = Llamada.objects.all().order_by('-id')
    return render_to_response('reportes_sub.html',{'time':datetime.now(),'llamadas':llamadas}, context_instance=RequestContext(request))

@login_required
def volantes(request):
    dato = Volante.objects.filter(codu=request.user).order_by('-id')
    #vola = Gestor.objects.filter(registro=request.user).last()

    #if vola == empty:
    #    dato = 0
    #else:
    #    dato = Gestor.objects.filter(registro=request.user).last()
    return render_to_response('volantes.html',{'time':datetime.now(),'dato':dato}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def inicio(request):
    informes = Llamada.objects.all()
    info = Llamada.objects.count()

    asi = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['1']).count()
    xasi = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['0']).count()
    ate = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['3']).count()
    atg = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['5']).count()
    ats = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['6']).count()
    dev = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['7']).count()
    cer = RegistroCaso.objects.filter(codu=request.user).filter(flag21__in=['4']).count()

    asi1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['1']).count()
    xasi1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['0']).count()
    ate1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['3']).count()
    atg1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['5']).count()
    ats1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['6']).count()
    dev1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['7']).count()
    cer1 = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).filter(flag21__in=['4']).count()

    asi2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['1']).count()
    xasi2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['0']).count()
    ate2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['3']).count()
    atg2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['5']).count()
    ats2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['6']).count()
    dev2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['7']).count()
    cer2 = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).filter(flag21__in=['4']).count()

    mas = Masivo.objects.all().count()
    asi3 = 0
    xasi3 = 0
    ate3 = 0
    atg3 = 0
    ats3 = 0
    dev3 = 0
    cer3 = 0    
    
    individual = RegistroCaso.objects.filter(codu=request.user).count
    asignados = RegistroCaso.objects.filter(gestor_enc=request.user.get_full_name).count
    grupo = RegistroCaso.objects.filter(codgrupo=request.user.profile.codgrupo).count
    return render(request, "index.html", {'mas':mas,'atg':atg,'ats':ats,'dev':dev,'atg1':atg1,'ats1':ats1,'dev1':dev1,'atg2':atg2,'ats2':ats2,'dev2':dev2,'atg3':atg3,'ats3':ats3,'dev3':dev3,'time':datetime.now(),"informes": informes,'info':info,'individual':individual,'asignados':asignados,'grupo':grupo,'asi':asi,'ate':ate, 'cer':cer, 'asi1':asi1,'ate1':ate1, 'cer1':cer1, 'asi2':asi2,'ate2':ate2, 'cer2':cer2, 'asi3':asi3,'ate3':ate3, 'cer3':cer3, 'xasi':xasi,'xasi1':xasi1,'xasi2':xasi2, 'xasi3':xasi3})

@login_required
def detalle(request, id):
    dato = get_object_or_404(Llamada, pk=id)
    cierre = CierreLlamada.objects.filter(llamada=dato)
    return render_to_response('detalle_llamada.html',{'dato':dato,'cierre':cierre}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def aplicativos(request):
    informes = Llamada.objects.all()
    info = Llamada.objects.count()
    return render(request, "aplicativos.html", {'time':datetime.now(),"informes": informes,'info':info})

@login_required(login_url='/ingresar')
def devoluciones(request):
    llamadas = Llamada.objects.all().order_by('-id')[0:1000]
    conteo = Llamada.objects.count()
    return render(request, "devoluciones.html", {'time':datetime.now(),"llamadas": llamadas,'conteo':conteo})

@login_required
def exportar(request):
    exportar = Llamada.objects.all().values('id', 'ruc','razon_social','telefono','contacto','titulo','descripcion','fecha_ingreso','cisco','tema','gestor','estado')
    with open('Devolucion.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)

@login_required
def exportar_llamada(request):
    exportar = LlamadaLog.objects.all().values('id_llamada','id_adicional', 'ruc','razon_social','telefono','contacto','titulo','descripcion','fecha_ingreso','cisco','tema','gestor','estado','anexo','hora','respuesta')
    with open('Devolucion.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)

@login_required
def exportar_volante(request):
    exportar = Volante.objects.all().values('id', 'registro','nombres','fecha_act','hora_ini','hora_fin','usuario','anexo')
    with open('volantes.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos_rpta(request):
    exportar = RegistroCaso.objects.filter(flag21='4').values('code','ruc','razon_social','titulo','descripcion','cisco','tema','respuesta')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos(request):
    exportar = RegistroCaso.objects.all()
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos1(request):
    exportar = RegistroCaso.objects.filter(cisco='T Registro')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos2(request):
    exportar = RegistroCaso.objects.filter(cisco='PLAME')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos3(request):
    exportar = RegistroCaso.objects.filter(cisco='Essalud - ONP - SIS')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos4(request):
    exportar = RegistroCaso.objects.filter(cisco='Detracciones')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos5(request):
    exportar = RegistroCaso.objects.filter(cisco='Fraccionamiento - DDJJ Anuales e Informativas')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos6(request):
    exportar = RegistroCaso.objects.filter(cisco='RUC')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos7(request):
    exportar = RegistroCaso.objects.filter(cisco='PDT - Declara Fácil')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos8(request):
    exportar = RegistroCaso.objects.filter(cisco='PDB')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos9(request):
    exportar = RegistroCaso.objects.filter(cisco='COA')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos10(request):
    exportar = RegistroCaso.objects.filter(cisco='Otros Temas')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos11(request):
    exportar = RegistroCaso.objects.filter(cisco='Valicentro')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos12(request):
    exportar = RegistroCaso.objects.filter(cisco='Extranet')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos13(request):
    exportar = RegistroCaso.objects.filter(cisco='Nuevo SEMT - Retención con terceros')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos14(request):
    exportar = RegistroCaso.objects.filter(cisco='SEE (Del Contribuyente)')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos15(request):
    exportar = RegistroCaso.objects.filter(cisco='SEE (Portal)')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos16(request):
    exportar = RegistroCaso.objects.filter(cisco='SLE - Sistema de Libro Electrónicos')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos17(request):
    exportar = RegistroCaso.objects.filter(cisco='IQBF - Insumos Químicos y Bienes Fiscalizados')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos18(request):
    exportar = RegistroCaso.objects.filter(cisco='Autorizición de CdP / Actualización Estado de Imprenta')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos19(request):
    exportar = RegistroCaso.objects.filter(cisco='Centrales de Riesgo / Requerimientos de Pago')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos20(request):
    exportar = RegistroCaso.objects.filter(cisco='Supervisor Edgar')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos21(request):
    exportar = RegistroCaso.objects.filter(cisco='Supervisor Javier')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos22(request):
    exportar = RegistroCaso.objects.filter(cisco='PSE')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos23(request):
    exportar = RegistroCaso.objects.filter(cisco='OSE')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_casos24(request):
    exportar = RegistroCaso.objects.filter(cisco='Gestor de Cumplimiento')
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_tramite(request):
    exportar = ReporteTramite.objects.all()
    with open('registro_tramites.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_chat(request):
    exportar = ReporteChat.objects.all()
    with open('registro_chat.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))

@login_required
def exportar_chat_sup(request):

    minimo = datetime.strptime(request.GET['minimo'], '%Y-%m-%d')
    maximo = datetime.strptime(request.GET['maximo'], '%Y-%m-%d')

    if minimo and maximo:
        exportar = ReporteChat.objects.filter(Q(fecha__range=(minimo,maximo))).order_by('-id')
    else:
        exportar = []

    with open('registro_chat_sup.csv', 'w') as csv_file:
        return render_to_csv_response(exportar)
    return render_to_response('supervisor.html',{'dato':dato,"exportar": exportar}, context_instance=RequestContext(request))
    
@login_required(login_url='/ingresar')
def devolucionllamadas(request):
    conteo = Llamada.objects.count()

    if conteo == 0:
        conteo = 1
    else:
        conteo = Llamada.objects.count() + 1

    if request.method=='POST':
        formulario = LlamadaForm(request.POST, request.FILES)
        Llamada(
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            gestor = request.user.get_full_name(),
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            flag = request.POST["flag"],
            code = request.POST["code"],
            codu = request.user
        ).save()
        LlamadaLog(
            id_llamada = request.POST["id_llamada"],
            id_adicional = request.POST["id_adicional"],
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            telefono = request.POST["telefono"],
            contacto = request.POST["contacto"],
            titulo = request.POST["titulo"],
            code = request.POST["code"],
            descripcion = request.POST["descripcion"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            cisco = request.POST["cisco"],
            tema = request.POST["tema"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            gestor = request.user.get_full_name(),
            adjunto = request.FILES.get('adjunto', '0'),
            #adjunto = request.FILES.get('estado', '0'),
            uuoo = request.POST["uuoo"],
            grupo = request.POST["grupo"],
            flag = request.POST["flag"],
            codu = request.user
        ).save()
        return HttpResponseRedirect('/devoluciones')
    else:
        formulario = LlamadaForm()
    return render(request, "devolucion_llamadas.html", {'conteo':conteo,'time':datetime.now()})

@login_required
def redevolucion(request, id):
    llama = Llamada.objects.get(pk=id)
    conteo = LlamadaLog.objects.filter(id_llamada=id).count()

    if conteo == 0:
        conteo = 1
    else:
        conteo = LlamadaLog.objects.filter(id_llamada=id).count() 

    
    if request.method=='POST':
        formulario = CierreLlamadaForm(request.POST)
        CierreLlamada(
            llamada = llama,
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            respuesta = request.POST["respuesta"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            flag2 = request.POST["flag2"],
            gestor = request.POST["gestor"],
            code = request.POST["code"],
            codu = request.user
        ).save()
        LlamadaLog(
            id_llamada = request.POST["id_llamada"],
            id_adicional = request.POST["id_adicional"],
            ruc = request.POST["ruc"],
            razon_social = request.POST["razon_social"],
            respuesta = request.POST["respuesta"],
            fecha_ingreso = request.POST["fecha_ingreso"],
            estado = request.POST["estado"],
            hora = request.POST["hora"],
            anexo = request.POST["anexo"],
            flag2 = request.POST["flag2"],
            gestor = request.POST["gestor"],
            code = request.POST["code"],
            codu = request.user
        ).save()
        #actu = Llamada.objects.filter(pk=id).update(estado='Con Éxito')
        return HttpResponseRedirect('/devoluciones')
    else:
        formulario = CierreLlamadaForm()
    return render_to_response('cierrellamada.html',{'formulario':formulario, 'conteo':conteo ,'llama':llama,'time':datetime.now()}, context_instance=RequestContext(request))

def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/inicio')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/inicio')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('inicio.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required
def editar_contrasena(request):
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
        return HttpResponseRedirect('/inicio')
    else:
        form = EditarContrasenaForm()
    return render_to_response('editar_contrasena.html', {'form': form}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


from django.views.defaults import page_not_found
 
def mi_error_404(request):
    nombre_template = 'volantes.html'
 
    return page_not_found(request, template_name=nombre_template)