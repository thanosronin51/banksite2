from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone


User = settings.AUTH_USER_MODEL


class Diposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )

    target = models.CharField(max_length=200)

    recipient_bank_name = models.CharField(max_length=200, default='')

    account_number = models.CharField(max_length=200, default='')

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Withdrawal.objects.get(pk=self.pk).status
            if old_status == 'completed' and self.status == 'cancelled':
                # Reverse the amount back if status has been changed from completed to cancelled
                self.user.balance += self.amount
            elif old_status == 'cancelled' and self.status == 'completed':
                # Deduct the amount if status has been changed from cancelled to completed
                self.user.balance -= self.amount
            else:
                # No status change, do nothing
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Manage Transfer"
        verbose_name_plural = "Manage Transfers"

@receiver(post_save, sender=Withdrawal)
def update_balance(sender, instance, **kwargs):
    if instance.status == 'completed':
        user = instance.user
        user.balance -= instance.amount
        user.save()
    elif instance.status == 'cancelled':
        user = instance.user
        user.balance += instance.amount
        user.save()



class Withdrawal_internationa(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        related_name='withdrawals_international',
        on_delete=models.CASCADE,
    )

    target = models.CharField(max_length=200)

    recipient_bank_name = models.CharField(max_length=200, default='')

    account_number = models.CharField(max_length=200, default='')

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Withdrawal_internationa.objects.get(pk=self.pk).status
            if old_status == 'completed' and self.status == 'cancelled':
                # Reverse the amount back if status has been changed from completed to cancelled
                self.user.balance += self.amount
            elif old_status == 'cancelled' and self.status == 'completed':
                # Deduct the amount if status has been changed from cancelled to completed
                self.user.balance -= self.amount
            else:
                # No status change, do nothing
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Manage Transfer_international"
        verbose_name_plural = "Manage Transfers_international"

@receiver(post_save, sender=Withdrawal_internationa)
def update_balance(sender, instance, **kwargs):
    if instance.status == 'completed':
        user = instance.user
        user.balance -= instance.amount
        user.save()
    elif instance.status == 'cancelled':
        user = instance.user
        user.balance += instance.amount
        user.save()


class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.amount} for {self.reason}"

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('USDT_ERC20', 'USDT ERC20'),
        ('USDT_TRC20', 'USDT TRC20'),
        ('ETHEREUM', 'Ethereum'),
        ('BITCOIN', 'Bitcoin')
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    proof_of_pay = models.ImageField(upload_to='proofs/', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} paid {self.amount} via {self.payment_method}"
    
    def update_balance(self):
        if self.status == 'COMPLETE':
            self.user.balance += self.amount
            self.user.save()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Manage Deposit/Payment"
        verbose_name_plural = "Manage Deposit/Payment"