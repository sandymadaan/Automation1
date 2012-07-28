from django.contrib import admin
from Automation.tcc.models import *

class ClientJobAdmin(admin.ModelAdmin):
    list_display = ('job_no', 'client','type_of_consultancy','site' )
    search_fields = ('job_no',)
    list_filter = ['date']

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','address_1','address_2','state','city' )
    search_fields = ('name','city')
    list_filter = ['name']

class AmountAdmin(admin.ModelAdmin):
    list_display = ('job_no', 'lab','field','total' )
    search_fields = ('job_no',)
    list_filter = ['job_no']


class LabAdmin(admin.ModelAdmin):
    list_display = ('code', 'name' )
    search_fields = ('code',)
    list_filter = ['code']

class FieldAdmin(admin.ModelAdmin):
    list_display = ('lab','code', 'name' )
    search_fields = ('code',)
    list_filter = ['code']

class TestAdmin(admin.ModelAdmin):
    list_display = ('field','code', 'name','quantity','unit','cost' )
    search_fields = ('code',)
    list_filter = ['code']

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name','address', 'phone','director')
    search_fields = ('name',)
    list_filter = ['name']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('organisation','name','address', 'phone','dean','faxno')
    search_fields = ('name',)
    list_filter = ['name']

class StaffAdmin(admin.ModelAdmin):
    list_display = ('department','code', 'name','daily_income','position','lab')
    search_fields = ('code',)
    list_filter = ['code']

admin.site.register(Lab, LabAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(ClientJob, ClientJobAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Staff, StaffAdmin)

