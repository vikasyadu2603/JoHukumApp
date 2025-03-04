from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# richa start
class UserAdmin(BaseUserAdmin):
    model = User  # Explicitly define the model

    list_display = ('email', 'full_name', 'user_type', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active', 'user_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'mobile_no', 'address')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Other Info', {'fields': ('user_type', 'referral_code', 'unique_code',  'range_field')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'mobile_no', 'user_type', 'password1','password2'),
        }),
    )
    search_fields = ('email', 'full_name', 'user_type')
    ordering = ('user_id',)
    filter_horizontal = ()
    

admin.site.register(User, UserAdmin)

# richa end





#start
admin.site.register(BookingSlot)
admin.site.register(ConfirmBooking)
# end

#ankit start
admin.site.register(Service)


