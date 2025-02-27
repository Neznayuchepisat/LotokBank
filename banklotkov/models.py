from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile" 
    
    def save(self, *args, **kwargs):
        # Если это новый профиль, создаем его
        if not self.pk and not self.avatar:
            self.avatar = None
        super(Profile, self).save(*args, **kwargs)
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availible = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('purchase', 'Purchase')
        ('transfer', 'Transfer'),
        ('credit', 'Credit'),
        ('tax', 'Tax'),
        ('fine', 'Fine'),
        ('loan', 'Loan Disbursement'),
        ('repayment', 'Loan Repayment'),
    ]
    sender = models.ForeignKey(Profile, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, related_name='recived_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        sender_name = self.sender.user.username if self.sender else 'Bank'
        recipient_name = self.recipient.user.username if self.recipient else 'Bank'
        return f'[{self.created_at}] {sender_name} -> {recipient_name} : {self.amount}'
    

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"Review by {self.author.user.username} on {self.product.name}"
    

class BalanceRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Balance request for {self.user.username}: {self.amount}"


class Loan(models.Model):
    borrower = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField()  # срок кредита в днях
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    amount_repaid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            interest = self.amount * self.interest_rate / 100
            self.total_amount_due = self.amount + interest
        super().save(*args, **kwargs)

    def remaining_amount(self):
        return self.total_amount_due - self.amount_repaid

    def __str__(self):
        return f"Loan for {self.borrower.user.username}: {self.amount}"
    