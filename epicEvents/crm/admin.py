from django.contrib import admin
from crm.models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company_name", "id")


admin.site.register(Client, ClientAdmin)


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "is_signed",
        "display_sales_contact",
        "id",
    )

    def display_sales_contact(self, obj):
        if obj.sales_contact:
            return f"{obj.sales_contact.username} (ID: {obj.sales_contact.id})"
        return "N/A"

    display_sales_contact.short_description = "Sales Contact"

    def save_model(self, request, obj, form, change):
        if not obj.sales_contact:
            obj.sales_contact = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Contract, ContractAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ("contract", "location", "id")


admin.site.register(Event, EventAdmin)
