from django.contrib import admin

# Register your models here.


from .models import UserProfile, Banner, EmailVerifyRecord


class UserProfileAdmin(admin.ModelAdmin):
    pass


class BannerAdmin(admin.ModelAdmin):
    pass


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
