#from django.views import ListView

from django.http import Http404
from django.views.generic import ListView,DetailView
from django.shortcuts import render,get_object_or_404

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from .models import Product
# Create your views here.



class ProductFeaturedListView(ListView):
    queryset = Product.objects.all()
    template_name= "products/list.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.featured()
class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
    #queryset = Product.objects.all()
    template_name= "products/featured-detail.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.featured()



class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name= "products/list.html"

def product_list_view(request):
    queryset= Product.objects.all()
    context = {
    'object_list': queryset
    }
    return render(request,"products/list.html",context)

class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self,*args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404_id(Product,slug=slug)
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('Not found..')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()

        except:
            raise Http404('hmmmm')
        #object_viewed_signal.send(instance.__class__,instance=instance,request=request)
        return instance

class ProductDetailView(ObjectViewedMixin,DetailView):
    #queryset = Product.objects.all()
    template_name= "products/detail.html"
    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        print(context)
        return context

    def get_object(self,*args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('Product does not exists')
        return instance


def product_detail_view(request,pk=None,*args,**kwargs):
    instance= Product.objects.get(pk=pk)
    instance = get_object_or_404(Product,pk=pk)
    """try:
        instance = Product.objects.get(id=4)
    except Product.DoesNotExist:
        print('Product doesnt exists')
        raise Http404('Product does not exists')
    except:
        print('Check for another product')"""

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('Product does not exists')
    print(instance)
    qs = Product.objects.filter(id=pk)

    print(qs)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404('Product does not exists')


    context = {
    'object': instance
    }
    return render(request,"products/detail.html",context)
