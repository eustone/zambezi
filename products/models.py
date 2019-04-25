from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from ecommerce.utils import unique_slug_generator

# Create your models here.
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)
    def search(self, query):
        lookups = (Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(price__icontains=query) |
                  Q(tag__title__icontains=query)
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()
class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured=True)
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    def search(self,query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(lookups)

class Product(models.Model):
    title       = models.CharField(max_length=120)
    description = models.TextField()
    slug        = models.SlugField(blank=True,unique=True)
    price       = models.DecimalField(decimal_places=2,max_digits=10,default=39.99)
    image       = models.ImageField(upload_to='products/',null=True,blank=True)
    featured    = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return '/products/{slug}/'.format(slug=self.slug)
        return reverse('products:detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect( product_pre_save_receiver,sender=Product)
