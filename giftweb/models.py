
from django.db import models
from ckeditor.fields import RichTextField

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    countdown_time = models.DurationField()
    image = models.ImageField(upload_to='product_images')
    timestamp = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class PremiumProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    countdown_time = models.DurationField()
    image = models.ImageField(upload_to='product_images')
    extra_feature = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete')
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    premium_product = models.ForeignKey(PremiumProduct, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    proof_of_pay = models.ImageField(upload_to='photos/', null=True, blank=True)
    gift_card_type = models.CharField(choices=[('apple', 'Apple Card'), ('amazon', 'Amazon Card'), ('steam', 'Steam Card'), ('xbox', 'Xbox Card')], max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def mark_as_complete(self):
        self.completed = True
        self.save()
    def __str__(self):
        return f"{self.user} paid {self.amount} for {self.product}"

    class Meta:
        verbose_name = "Manage Deposit/Payment"
        verbose_name_plural = "Manage Deposit/Payment"


class CartItem(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    premium_product = models.ForeignKey(PremiumProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart item {self.id} - User: {self.user.username}, Product: {self.product.name}"

class Blog(models.Model):
    topic = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images')
    body = RichTextField()
    date = models.DateField()
    read_more = models.CharField(max_length=255, default='GiftCard')

    def __str__(self):
        return self.topic