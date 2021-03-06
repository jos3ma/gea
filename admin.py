from django.contrib import admin
from grappelli_nested.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.http import HttpResponse, HttpResponseRedirect

# Register your models here.

from gea.models import Antecedente, Catastro, CatastroLocal, Circunscripcion, Dp, Ds, Sd, Expediente, ExpedienteLugar, ExpedienteObjeto, ExpedientePartida, ExpedientePersona, ExpedienteProfesional, Lugar, Objeto, Partida, PartidaDominio, Persona, Profesional, Titulo, Zona


from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Q


#
# Custom Filters
#

# Expedientes

class InscriptoFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('inscripto')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'inscripto'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'si':
            return queryset.filter(inscripcion_numero__isnull=False)
        if self.value() == 'no':
            return queryset.filter(inscripcion_numero__isnull=True)

class TieneOrdenFilter(admin.SimpleListFilter):
    title = _('tiene orden')
    parameter_name = 'orden'
    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(orden_numero__isnull=False)
        if self.value() == 'no':
            return queryset.filter(orden_numero__isnull=True)

class TieneOrdenPendienteFilter(admin.SimpleListFilter):
    title = _('orden pendiente')
    parameter_name = 'orden_pendiente'
    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(orden_numero__isnull=False, inscripcion_numero__isnull=True)
        if self.value() == 'no':
            return queryset.exclude(orden_numero__isnull=False, inscripcion_numero__isnull=True)

class TieneAntecedentesFilter(admin.SimpleListFilter):
    title = _('tiene antecedentes')
    parameter_name = 'antecedente'
    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(antecedente__isnull=False)
        if self.value() == 'no':
            return queryset.filter(antecedente__isnull=True)

class TieneObjetoFilter(admin.SimpleListFilter):
    title = _('tiene objeto')
    parameter_name = 'objeto'
    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.filter(expedienteobjeto__isnull=False)
        if self.value() == 'no':
            return queryset.filter(expedienteobjeto__isnull=True)

class TienePlanoFilter(admin.SimpleListFilter):
    title = _('tiene plano cargado')
    parameter_name = 'plano'
    def lookups(self, request, model_admin):
        return (
            ('si', _('Si')),
            ('no', _('No')),
        )
    def queryset(self, request, queryset):
        if self.value() == 'si':
            return queryset.exclude(plano_ruta__isnull=True).exclude(plano_ruta__exact='')
        if self.value() == 'no':
            return queryset.filter(Q(plano_ruta__isnull=True) | Q(plano_ruta__exact=''))

# Personas
class CantidadDeExpedientesFilter(admin.SimpleListFilter):
    title = _('cantidad de expedientes')
    parameter_name = 'expedientes'
    def lookups(self, request, model_admin):
        return (
            ('0', _('Ninguno')),
            ('1', _('1')),
            ('2', _('2')),
            ('3', _('3')),
            ('4+', _('4 o +')),
        )
    def queryset(self, request, queryset):
        qs = queryset.annotate(entry_count=Count('expedientepersona'))
        if self.value() == '0':
            qs = qs.filter(entry_count=0)
            return qs
        if self.value() == '1':
            qs = qs.filter(entry_count=1)
            return qs
        if self.value() == '2':
            qs = qs.filter(entry_count=2)
            return qs
        if self.value() == '3':
            qs = qs.filter(entry_count=3)
            return qs
        if self.value() == '4+':
            qs = qs.filter(entry_count__gt=3)
            return qs

class AntecedenteAdmin(admin.ModelAdmin):
    list_display = ('expediente', 'expediente_modificado', 'inscripcion_numero', 'duplicado', 'obs', 'plano_ruta')
    list_editable = ('expediente_modificado', 'inscripcion_numero', 'duplicado', 'obs', 'plano_ruta')
    search_fields = ['expediente__id', 'expediente_modificado__id', 'inscripcion_numero', 'duplicado', 'obs']
    actions_on_bottom = True
    list_per_page = 20
    save_on_top = True
    ordering = ['expediente', '-expediente_modificado', 'inscripcion_numero']
    def show_plano_ruta(self, obj):
        if obj.plano_ruta != '' and obj.plano_ruta != None:
            return '<a href="%s">%s</a>' % (obj.plano_ruta, obj.inscripcion_numero)
        else:
            return obj.plano_ruta
    show_plano_ruta.allow_tags = True
    show_plano_ruta.short_description = 'Plano'
admin.site.register(Antecedente, AntecedenteAdmin)
#admin.site.register(Catastro)
# class CatastroLocalAdmin(admin.ModelAdmin):
    # list_display = ('seccion', 'manzana', 'parcela', 'subparcela', 'suburbana', 'poligono')
    # list_filter = ['seccion']
    # search_fields = ['seccion', 'manzana', 'parcela', 'subparcela', 'suburbana', 'poligono']
# admin.site.register(CatastroLocal, CatastroLocalAdmin)
class CircunscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'orden')
    #list_editable = ('nombre', 'orden')
    search_fields = ['id', 'nombre', 'orden']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Circunscripcion, CircunscripcionAdmin)
class DpAdmin(admin.ModelAdmin):
    list_display = ('dp', 'nombre', 'habitantes', 'superficie', 'cabecera', 'circunscripcion')
    #list_editable = ('nombre', 'habitantes', 'superficie', 'cabecera', 'circunscripcion')
    list_filter = ['circunscripcion', 'circunscripcion__orden']
    search_fields = ['dp', 'nombre', 'habitantes', 'superficie', 'cabecera', 'circunscripcion__nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Dp, DpAdmin)
class DsAdmin(admin.ModelAdmin):
    list_display = ('id', 'dp', 'ds', 'nombre')
    #list_editable = ('nombre',)
    list_filter = ['dp', 'dp__nombre']
    search_fields = ['dp__nombre', 'ds', 'nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Ds, DsAdmin)
class SdAdmin(admin.ModelAdmin):
    list_display = ('id', 'ds', 'sd', 'nombre')
    #list_editable = ('nombre',)
    list_filter = ['ds__dp', 'ds__dp__nombre', 'ds', 'ds__nombre']
    search_fields = ['ds__nombre', 'sd', 'nombre', 'ds__dp__nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Sd, SdAdmin)
class CatastroLocalInline(NestedStackedInline):
    model = CatastroLocal
    extra = 0
class ExpedienteLugarInline(NestedTabularInline):
    model = ExpedienteLugar
    extra = 0
    inlines = [CatastroLocalInline]
class ExpedienteObjetoInline(NestedTabularInline):
    model = ExpedienteObjeto
    extra = 0
class ExpedientePersonaInline(NestedTabularInline):
    model = ExpedientePersona
    extra = 0
    ordering = ['-comitente']
class ExpedienteProfesionalInline(NestedTabularInline):
    model = ExpedienteProfesional
    extra = 0
class CatastroInline(NestedStackedInline):
    model = Catastro
    extra = 0
class ExpedientePartidaInline(NestedTabularInline):
    model = ExpedientePartida
    extra = 0
    inlines = [CatastroInline]
class AntecedenteInline(NestedTabularInline):
    model = Antecedente
    fk_name = 'expediente'
    extra = 0
    ordering = ['-expediente_modificado', '-inscripcion_numero']
class ExpedienteAdmin(NestedModelAdmin):
    fieldsets = [
        (None,       {'fields': [('id', 'fecha_plano', 'mensuras')], 'classes': ('extrapretty')}),
        ('Catastro', {'fields': [('inscripcion_numero', 'inscripcion_fecha', 'duplicado', 'sin_inscripcion')], 'classes': ('extrapretty')}),
        ('Colegio',  {'fields': [('orden_numero', 'orden_fecha')], 'classes': ('extrapretty')}),
        ('Otros',    {'fields': [('cancelado', 'cancelado_por'), 'plano_ruta'], 'classes': ('extrapretty')}),
    ]
    inlines = [ExpedienteLugarInline, ExpedienteObjetoInline, ExpedientePersonaInline, ExpedienteProfesionalInline, ExpedientePartidaInline, AntecedenteInline]
    list_display = ('id', 'fecha_plano', 'inscripcion_numero', 'inscripcion_fecha', 'duplicado', 'sin_inscripcion', 'orden_numero', 'orden_fecha', 'cancelado', 'show_plano_ruta')
    list_editable = ('fecha_plano', 'inscripcion_numero', 'inscripcion_fecha', 'duplicado', 'orden_numero', 'orden_fecha', 'sin_inscripcion', 'cancelado')
    list_filter = [InscriptoFilter, 'duplicado', 'sin_inscripcion', TieneOrdenFilter, TieneOrdenPendienteFilter, 'cancelado', 'cancelado_por', TienePlanoFilter, 'expedientelugar__catastrolocal__seccion', 'expedientelugar__catastrolocal__manzana', 'expedientelugar__catastrolocal__parcela', TieneObjetoFilter, TieneAntecedentesFilter]
    search_fields = ['id', 'fecha_plano', 'inscripcion_numero', 'inscripcion_fecha', 'orden_numero', 'orden_fecha', 'cancelado_por', 'expedientelugar__lugar__nombre', 'expedientepersona__persona__apellidos', 'expedientepersona__persona__nombres', 'expedientepersona__persona__apellidos_alternativos', 'expedientepersona__persona__nombres_alternativos', 'expedienteprofesional__profesional__apellidos', 'expedienteobjeto__objeto__nombre', 'expedientepartida__partida__pii', 'antecedente__expediente_modificado__id', 'antecedente__inscripcion_numero']
    actions_on_bottom = True
    date_hierarchy = 'inscripcion_fecha'
    list_per_page = 20
    save_on_top = True
    def show_plano_ruta(self, obj):
        if obj.plano_ruta != '' and obj.plano_ruta != None:
            return '<a href="%s">%s</a>' % (obj.plano_ruta, obj.inscripcion_numero)
        else:
            return obj.plano_ruta
    show_plano_ruta.allow_tags = True
    show_plano_ruta.short_description = 'Plano'
admin.site.register(Expediente, ExpedienteAdmin)
class ExpedienteLugarAdmin(admin.ModelAdmin):
    inlines = [CatastroLocalInline]
    list_display = ('expediente', 'lugar')
    list_filter = ['catastrolocal__seccion', 'catastrolocal__manzana', 'catastrolocal__parcela']
    search_fields = ['expediente__id', 'lugar__nombre']
    actions_on_bottom = True
    list_per_page = 20
    save_on_top = True
admin.site.register(ExpedienteLugar, ExpedienteLugarAdmin)
#admin.site.register(ExpedienteObjeto)
class ExpedientePartidaAdmin(admin.ModelAdmin):
    inlines = [CatastroInline]
    list_display = ('expediente', 'partida')
    search_fields = ['expediente__id', 'partida__pii']
    list_select_related = True
    list_per_page = 20
admin.site.register(ExpedientePartida, ExpedientePartidaAdmin)
#admin.site.register(ExpedientePersona)
#admin.site.register(ExpedienteProfesional)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'obs')
    list_editable = ('obs',)
    search_fields = ['nombre', 'obs']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Lugar, LugarAdmin)
class ObjetoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Objeto, ObjetoAdmin)
class PartidaDominioInline(admin.TabularInline):
    model = PartidaDominio
    extra = 0
class PartidaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [('sd', 'pii', 'subpii', 'api')]}),
    ]
    inlines = [PartidaDominioInline]
    list_filter = ['sd__ds__dp__nombre']
    search_fields = ['pii', 'sd__nombre', 'sd__ds__nombre', 'sd__ds__dp__nombre']
    actions_on_bottom = True
    save_on_top = True
    list_per_page = 20
    list_select_related = True
admin.site.register(Partida, PartidaAdmin)
#admin.site.register(PartidaDominio)
class PersonaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': [('apellidos', 'nombres'), ('apellidos_alternativos', 'nombres_alternativos')]}),
        ('Contacto',          {'fields': [('domicilio', 'lugar'), ('telefono', 'celular'), 'email']}),
        ('DNI/CUIT/CUIL/CDI', {'fields': ['cuit_cuil']}),
    ]
    inlines = [ExpedientePersonaInline]
    list_display = ('nombre_completo', 'domicilio', 'lugar', 'telefono', 'celular', 'email', 'cuit_cuil')
    #list_editable = ('domicilio', 'lugar', 'telefono', 'celular', 'email', 'cuit_cuil')
    list_filter = [CantidadDeExpedientesFilter, 'lugar']
    search_fields = ['nombres', 'apellidos', 'nombres_alternativos', 'apellidos_alternativos', 'domicilio', 'telefono', 'celular', 'email', 'cuit_cuil', 'expedientepersona__expediente__id']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Persona, PersonaAdmin)
class ProfesionalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': [('apellidos', 'nombres'), ('titulo', 'icopa')]}),
        ('Contacto',          {'fields': [('domicilio', 'lugar'), ('telefono', 'celular'), ('email', 'web')]}),
        ('DNI/CUIT/CUIL/CDI', {'fields': ['cuit_cuil']}),
        ('Otra info',         {'fields': [('habilitado', 'jubilado', 'fallecido')]}),
    ]
    list_display = ('nombre_completo', 'titulo', 'icopa', 'domicilio', 'lugar', 'telefono', 'celular', 'email', 'web', 'cuit_cuil')
    #list_editable = ('titulo', 'icopa', 'domicilio', 'lugar', 'telefono', 'celular', 'email', 'web', 'cuit_cuil')
    list_filter = ['habilitado', 'jubilado', 'fallecido', 'titulo__nombre', 'lugar']
    search_fields = ['nombres', 'apellidos', 'icopa', 'domicilio', 'telefono', 'celular', 'email', 'web', 'cuit_cuil']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Profesional, ProfesionalAdmin)
admin.site.register(Titulo)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion')
    #list_editable = ('descripcion',)
    search_fields = ['id', 'descripcion']
    actions_on_bottom = True
    save_on_top = True
admin.site.register(Zona, ZonaAdmin)
