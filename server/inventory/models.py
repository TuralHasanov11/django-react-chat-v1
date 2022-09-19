from django.db import models
from django.contrib.postgres import indexes as postgresIndexes

# Create your models here.
class Brand(models.Model):
    name = models.CharField("Brand Name", max_length=50)
    slug = models.SlugField()
    is_active = models.BooleanField(null=False, blank=True, default=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField("Category Name", max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    is_active = models.BooleanField(null=False, blank=True, default=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField("Product Name", max_length=100, default="no-name", help_text="This is the help text")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(null=False, blank=True, default=True)
    brand = models.ForeignKey(Brand, on_delete=models.RESTRICT)
    category = models.ManyToManyField(Category)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["age"]
        indexes = [  
          postgresIndexes.GinIndex(name='ProductGinIndex', fields=['name'], opclasses=['gin_trgm_ops']),
        ]
    
    def __str__(self):
        return {self.name}


class ProductAttribute(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    value = models.CharField(max_length=50)

    attribute = models.ForeignKey(
        ProductAttribute, related_name="product_attribute", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.value
    

class Inventory(models.Model):
    is_active = models.BooleanField()
    is_default = models.BooleanField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    sku = models.CharField(
        max_length=20,
        unique=True,
    )
    # sku = models.UUIDField(default=uuid.uuid4, editable=False)

    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )
    attribute_values = models.ManyToManyField(ProductAttributeValue)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory"

    def __str__(self):
        return self.product.name


class StockControl(models.Model):
    last_checked = models.DateTimeField(auto_now_add=False, editable=False)
    units = models.IntegerField(default=0)
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Stock Control"


class ProductImage(models.Model):
    url = models.ImageField(upload_to=None)
    alternative_text = models.CharField(max_length=50)
    is_feature = models.BooleanField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)