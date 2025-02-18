from django.contrib import admin
from .models import Profile, Product, Transaction, BalanceRequest, Loan

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'amount', 'availible')
    list_filter = ('availible',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('sender__user__username', 'recipient__user__username')

@admin.register(BalanceRequest)
class BalanceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username',)
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for balance_request in queryset:
            if not balance_request.approved:
                profile = Profile.objects.get(user=balance_request.user)
                profile.balance += balance_request.amount
                profile.save()
                balance_request.approved = True
                balance_request.save()
        self.message_user(request, f"{queryset.count()} запросов на пополнение баланса одобрено.")
    approve_requests.short_description = "Одобрить выбранные запросы на пополнение баланса"

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'amount', 'term', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('borrower__user__username',)