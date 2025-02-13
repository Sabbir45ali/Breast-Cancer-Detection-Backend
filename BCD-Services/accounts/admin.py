from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# Change this to import the model
from .models import CustomUserModel  

# Custom admin configuration for the user model
class UserAdminCustom(UserAdmin):
    
    # Customize fieldsets for user imformation in admin panel
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    # Customize add user form in admin panel
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
    
    # Customize list display & search fields
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    
    readonly_fields = ['date_joined', 'last_login']

# Make certain fields read-only
# Register the model, not the manager
admin.site.register(CustomUserModel, UserAdminCustom)  