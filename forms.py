#encoding:utf-8 
from django.forms import ModelForm
from django import forms
from principal.models import Profile, Llamada, Volante, Gestor, CierreLlamada, LlamadaLog, ReporteTramite, RespuestaTramite, ReporteChat, RegistroCaso, AsignarCaso, CierreCaso, Masivo, Consolidado
from django.contrib.auth.models import User


class EditarUserForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('codgrupo','grupo')

class MasivoForm(ModelForm):
    class Meta:
        model = Masivo
        fields = '__all__'
        
class RegistroCasoForm(ModelForm):
    class Meta:
        model = RegistroCaso
        fields = '__all__'

class AsignarCasoForm(ModelForm):
    class Meta:
        model = AsignarCaso
        fields = '__all__'

class EditarCasoIniForm(ModelForm):
    class Meta:
        model = RegistroCaso
        fields = ('code','ruc', 'razon_social', 'contacto','telefono','adjunto','cisco','tema','codgrupo','titulo','descripcion','fecha_ingreso')

class EditarCasoForm(ModelForm):
    class Meta:
        model = RegistroCaso
        fields = ('gestor_enc', 'fecha_asi', 'flag21')

class CierreCasoForm(ModelForm):
    class Meta:
        model = CierreCaso
        fields = '__all__'

class ReporteTramiteForm(ModelForm):
    class Meta:
        model = ReporteTramite
        fields = '__all__'

class RespuestaTramiteForm(ModelForm):
    class Meta:
        model = RespuestaTramite
        fields = '__all__'

class EditarTramiteForm(ModelForm):
    class Meta:
        model = RespuestaTramite
        fields = '__all__'

class ConsolidadoForm(ModelForm):
    class Meta:
        model = RespuestaTramite
        fields = '__all__'

class ReporteChatForm(ModelForm):
    class Meta:
        model = ReporteChat
        fields = '__all__'
        
class EditarChatForm(ModelForm):
    class Meta:
        model = ReporteChat
        fields = ('fecha','registro','tipo_doc', 'ruc', 'consulta','adjunto','tema','subtema','tema1','subtema1','tema2','subtema2','tema3','subtema3','contacto','correo','observa','hora_ini','hora_fin','hora_tot')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('supervision', 'grupo', 'uuoo')

class LlamadaForm(ModelForm):
    class Meta:
        model = Llamada
        fields = '__all__'

class EditarLlamadaForm(ModelForm):
    class Meta:
        model = Llamada
        fields = ('ruc', 'razon_social', 'contacto','telefono','hora','adjunto','anexo','cisco','tema','descripcion','estado')

class LlamadaLogForm(ModelForm):
    class Meta:
        model = LlamadaLog
        fields = '__all__'

class CierreLlamadaForm(ModelForm):
    class Meta:
        model = CierreLlamada
        fields = '__all__'

class GestorForm(ModelForm):
    class Meta:
        model = Gestor
        fields = '__all__'

class VolanteForm(ModelForm):
    class Meta:
        model = Volante
        fields = '__all__'
        fecha_act = forms.DateField(input_formats=['%d/%m/%Y'])
        
class EditarContrasenaForm(forms.Form):

    actual_password = forms.CharField(
        label='Contraseña actual',
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Nueva contraseña',
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir contraseña',
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2



