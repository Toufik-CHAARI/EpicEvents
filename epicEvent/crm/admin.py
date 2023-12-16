from django.contrib import admin
from crm.models import Client, Contract, Event



class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name","company_name")

admin.site.register(Client,ClientAdmin)


class ContractAdmin(admin.ModelAdmin):
    list_display = ("client","is_signed")

admin.site.register(Contract,ContractAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("contract","location")

admin.site.register(Event,EventAdmin)