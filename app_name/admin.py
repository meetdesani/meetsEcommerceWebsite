from django.contrib import admin
from .models import ContactUs, User, Product, WishList, Cart, ComplaintForm, Helpdesk, Checkout


class ContactUsModelAdmin(admin.ModelAdmin):
    list_display = ('email',)



class UserModelAdmin(admin.ModelAdmin):
    list_display= ('email', )
    
class UserModelProduct(admin.ModelAdmin):
    list_display= ('product_model', )
    


admin.site.register(ContactUs,ContactUsModelAdmin)
admin.site.register(User, UserModelAdmin)
admin.site.register(Product, UserModelProduct)
admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(ComplaintForm)
admin.site.register(Helpdesk)
admin.site.register(Checkout)
