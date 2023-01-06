import math
from django.conf import settings
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView,  TemplateView, FormView
from django.views.generic import CreateView


from .models import (Item, 
                    PurchaseOrder, 
                    Stock, 
                    SaleOrder, 
                    SaleOrderItem,
                    NewProduct, 
                    Product,
                    ItemPurchased)

from .forms import (PurchaseItemForm,
                   PurchaseOrderForm,
                   NewProductForm, 
                   ProductForm,
                   ItemCartForm,
                   PurchaseOrderUpdateForm,
                   ProductUpdateForm,
                   SaleOrderItemCreateForm,
                   SaleOrderCreateForm,
                   )


def round_up(x):
    return(int(math.ceil(x)))

class SlowveldFormsView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/slowveld_forms.html'


class PurchaseItemFormView(LoginRequiredMixin, CreateView):
    ''' Create View for new purchase items'''

    template_name = 'transactions/form_items/item_form.html'
    queryset = Item.objects.all()
    form_class = PurchaseItemForm
    success_url = reverse_lazy('transactions:purchase-order-list-view')

    def form_valid(self, form):
        
        if form.is_valid():
            item = form.cleaned_data['item']
            category = form.cleaned_data['category']
            uom_quantity  = form.cleaned_data['uom_quantity']
            uom = form.cleaned_data['uom']
            description = form.cleaned_data['description']
            cost_price = form.cleaned_data['cost_price']
            sold_in_packs = form.cleaned_data['sold_in_packs']

        purchaseItem = Item.objects.filter(item=item,category=category, uom=uom, cost_price=cost_price,uom_quantity=uom_quantity)
        if purchaseItem.exists():
            pItem = Item.objects.get(item=item,category=category, uom=uom)
            messages.warning(self.request, f'{item} ({uom_quantity} {uom}) already exists in list, item not added')
            return redirect("transactions:purchase-order-list-view")
        else:
            Item.objects.create(item=item,category=category,uom_quantity=uom_quantity,uom=uom,description=description,cost_price=cost_price, sold_in_packs=sold_in_packs)
            messages.success(self.request, f'{item} ({uom_quantity} {uom}) successfully added to items list')  
            return redirect("transactions:purchase-order-list-view")


class PurchaseOrderFormView(LoginRequiredMixin, FormView):
    ''' Add an item to a purchase form'''

    template_name = 'transactions/form_items/purchase_order_form.html'
    form_class = PurchaseOrderForm
    success_url = reverse_lazy('transactions:purchase-order-list-view')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.filter(~Q(uom_quantity_purchased=0))
        context["items"] = item
        # Order cost of the value of the unit
        order_cost = 0
        for i in item:
            
            order_cost += (i.cost_price/i.uom_quantity)*i.uom_quantity_purchased
            print(order_cost)
        context['order_cost'] = order_cost
        return context
    

    def form_valid(self, form, **kwargs):  
        if form.is_valid():
            all_items = Item.objects.all()
            order_cost = 0 + form.cleaned_data['delivery_price']
            item = form.cleaned_data['item']
            print(item)
            for items in all_items:
                if items.uom_quantity_purchased > 0:
                    order_cost += (items.cost_price/items.uom_quantity)*items.uom_quantity_purchased
            delivery_price  = form.cleaned_data['delivery_price']
            purchase_order_reference  = form.cleaned_data['purchase_order_reference']
            supplier = form.cleaned_data['supplier']


            instance = PurchaseOrder.objects.create(
                                                    delivery_price=delivery_price,
                                                    purchase_order_reference=purchase_order_reference,
                                                    supplier=supplier,
                                                    order_cost=order_cost,
                                                    
                                                    )
            
            for i in all_items:
                if i.uom_quantity_purchased > 0:
                    
                    instance.item.create(item=i.item,
                                         description=i.description,
                                         category = i.category,
                                         uom_quantity_purchased = i.uom_quantity_purchased,
                                         uom_quantity = i.uom_quantity,
                                         uom = i.uom,
                                         cost_price = (i.cost_price/i.uom_quantity)*i.uom_quantity_purchased,
                                         sold_in_packs=i.sold_in_packs
                                         )
            instance.save()
        
        messages.success(self.request,f'Order with ref #:{purchase_order_reference}, successfully created')
        
        for i in Item.objects.all():
            if i.uom_quantity_purchased > 0:
                Item.objects.filter(item=i.item).update(uom_quantity_purchased=0)





        return super().form_valid(form)    


class NewProductFormView(LoginRequiredMixin, FormView):
    '''Add input details of products'''
    
    template_name = 'transactions/form_items/new_product_form.html'
    form_class = NewProductForm
    model = NewProduct
    success_url = reverse_lazy('transactions:new-product-form')


    def form_valid(self, form):
        product_name = form.cleaned_data['product_name']
        input_item = form.cleaned_data['input_item']
        input_quantity = form.cleaned_data['input_quantity']
        product_type = product_name.product_type

        aProd = NewProduct.objects.filter(product_name=product_name,
                                            product_type = product_type,
                                            input_item=input_item,
                                )
        if not aProd.exists():
            nProd =   NewProduct.objects.create(product_name=product_name,
                                input_item=input_item,
                                input_quantity=input_quantity,
                                product_type = product_type,
                                    )
            product = Product.objects.get(name=nProd.product_name.name)


            new_prod = NewProduct.objects.latest('id')
            product.inputs.add(new_prod)
            messages.success(self.request,f'Product input: {input_item}, successfully created')
            return super().form_valid(form)
        else:
            messages.warning(self.request,f'Product input: {input_item} already exists, not added')
            return redirect("transactions:new-product-form")

 

class ProductUpdateView(LoginRequiredMixin, FormView):
    template_name = 'transactions/form_items/product_update_form.html'
    context_object = 'product'
    form_class = ProductUpdateForm
    success_url = reverse_lazy('transactions:product-update-form')

    def form_valid(self, form):
        if form.is_valid():
            # Update the Product stock on hand
            name = form.cleaned_data['name'] #.split('(',-1)[0]
            stock_on_hand  = form.cleaned_data['stock_on_hand']
            product = Product.objects.filter(name=name) 
            if product.exists():

                gProd = Product.objects.get(name=name)
                gProd.stock_on_hand += stock_on_hand
                product.update(stock_on_hand=gProd.stock_on_hand)

                p = Product.objects.filter(name=name)
                for i in p:
                    # Remove input quantity from Stock
                    for z in NewProduct.objects.filter(product_name=i):
                        nProd = NewProduct.objects.get(product_name=z.product_name, input_item_id=z.input_item_id)           
                        stock = Stock.objects.filter(item=nProd.input_item)
                        nprod_name = str(nProd.input_item).split('(',-1)[0].strip()
                        gStock = Stock.objects.get(item=nprod_name)
                        gStock.quantity_on_hand -= (nProd.input_quantity * stock_on_hand)
                        gStock.cost_price_on_hand -= (nProd.input_item.get_item_price() * (nProd.input_quantity * stock_on_hand))
                        stock.update(quantity_on_hand = gStock.quantity_on_hand,
                                    cost_price_on_hand= gStock.cost_price_on_hand )




        return redirect('transactions:product-list-view')

class ProductFormView(LoginRequiredMixin, FormView):
    ''' Create Finished Products'''

    template_name = 'transactions/form_items/product_form.html'
    model = Product
    form_class = ProductUpdateForm
    success_url = reverse_lazy('transactions:product-list-view')

    def form_valid(self, form):
        
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            stock_on_hand  = form.cleaned_data['stock_on_hand']
            product_type  = form.cleaned_data['product_type']

           

            product = Product.objects.filter(name=name,product_type=product_type)
            if product.exists():
                eProduct = Product.objects.get(name=name,product_type=product_type)
                eProduct.stock_on_hand += stock_on_hand
                product.update(name=name,
                            description=description,
                            stock_on_hand=eProduct.stock_on_hand,
                            product_type=eProduct.product_type)

                messages.success(self.request, f'{name} has been updated')
            else:
                ins= Product.objects.create(name=name,
                                        product_type=product_type,
                                        description=description,
                                        stock_on_hand=stock_on_hand,
                                        )
                messages.success(self.request, f'{name} ({stock_on_hand}) successfully added')  
            # Reduce stock by amount from NewProduct
            for i in ins.inputs.all():
                rStock = Stock.objects.filter(item=i)
                gStock = Stock.objects.get(item=i)
                gStock.quantity_on_hand -= stock_on_hand
                gStock.cost_price_on_hand -= ins.product_cost()
                rStock.update(quantity_on_hand=gStock.quantity_on_hand,
                                cost_price_on_hand=gStock.cost_price_on_hand)


            return redirect("transactions:product-list-view")   






# ==================================
#  ListViews


class PurchaseOrderListView(LoginRequiredMixin, ListView):
    model = PurchaseOrder
    template_name= 'transactions/purchase_order_list_view.html'
    context_object_name = 'purchases'



class ItemsListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "transactions/item_list_view.html"
    context_object_name = 'items'


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'transactions/stock_list_view.html'
    context_object_name = 'stock'

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "transactions/product_list_view.html"
    context_object_name = 'products'


class SaleOrderListView(LoginRequiredMixin, ListView):
    model = SaleOrder
    template_name = "transactions/sale_order_list_view.html"
    context_object_name = 'sales'


# ========================
# DETAILVIEWS




class ItemsDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'transactions/item_detail_view.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_form'] = ItemCartForm()
        return context


    def post(self, request, **kwargs):
        if request.method == 'POST': 
            item_form = ItemCartForm(request.POST)
            uItem = Item.objects.filter(id=self.kwargs.get('pk'))
            if uItem.exists:
                item_form.instance.post = Item.objects.get(id=self.kwargs.get('pk'))
                item = item_form.instance.post.item
                description = item_form.instance.post.description
                category = item_form.instance.post.category
                uom_quantity = item_form.instance.post.uom_quantity
                uom = item_form.instance.post.uom
                cost_price = item_form.instance.post.cost_price
                uom_quantity_purchased = item_form.instance.post.uom_quantity_purchased

                if item_form.instance.post.sold_in_packs:
                    if uom_quantity == int(item_form.instance.uom_quantity_purchased) + int(request.POST.get('uom_quantity_purchased')):
                        uom_quantity_purchased = int(item_form.instance.post.uom_quantity_purchased) + int(request.POST.get('uom_quantity_purchased'))
                    else:
                        uom_quantity_purchased += (round_up(int(request.POST.get('uom_quantity_purchased'))/int(uom_quantity))*int(uom_quantity))
                else:
                    uom_quantity_purchased = int(item_form.instance.post.uom_quantity_purchased) + int(request.POST.get('uom_quantity_purchased')) 
                
                uItem.update(item=item,
                            description=description,
                            category=category,
                            uom_quantity=uom_quantity,
                            uom=uom,
                            cost_price=cost_price,
                            uom_quantity_purchased=uom_quantity_purchased)
            return redirect('transactions:items-list-view')
        else:
            return redirect('transactions:items-list-view')


class  PurchaseOrderDetailview(LoginRequiredMixin, DetailView):
    template_name = "transactions/order_detail_view.html"
    model = PurchaseOrder
    context_object_name = 'order'


    

    def post(self, request, **kwargs):
        '''
        There is a form on the detailview of PurchaseOrder. 
        It redirects to the same page but toggles the boolean
        and add items to stock
        '''
        kw = self.kwargs['pk']
        if request.method == 'POST': 
            ins = PurchaseOrder.objects.get(id=kw)
            for i in ins.item.all():
                stock = Stock.objects.filter(item=i.item)
                if stock.exists():
                    oStock = get_object_or_404(Stock,item=i.item)
                    oStock.cost_price_on_hand += i.cost_price
                    oStock.quantity_on_hand +=i.uom_quantity_purchased
                    stock.update( quantity_on_hand = oStock.quantity_on_hand,
                                                    cost_price_on_hand=oStock.cost_price_on_hand ) 
                else:
                    Stock.objects.create(item=i.item,
                                        description =  i.description,
                                        category = i.category,
                                        supplier = i.supplier,
                                        quantity_on_hand = i.uom_quantity_purchased,
                                        uom = i.uom,
                                        cost_price_on_hand = i.cost_price,
                                        order_reference_id = ins.id,
                                        )
            if ins.received:
                ins.received = False
            else:
                ins.received = True
                for i in ins.item.all():
                    ItemPurchased.objects.filter(item=i.item,
                                              counted_as_stock=False,
                                              uom_quantity_purchased=i.uom_quantity_purchased,
                                              cost_price=i.cost_price).update(counted_as_stock = True)
            ins.save()  



            return  redirect('transactions:order-detail-view', pk=self.kwargs['pk'])
        else:
            return  redirect('transactions:order-detail-view',self.kwargs['pk'])


class SaleOrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "transactions/sale_order_detail_view.html"
    model = SaleOrder

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ins = SaleOrder.objects.get(id=self.kwargs['pk'])
        subtotal = 0
        for i in ins.product.all():
            subtotal += (i.pricing.sell_price * i.quantity)
        context["subtotal"] = subtotal
        return context
    

    def post(self, request, **kwargs):
        if request.method == 'POST': 
            print("POST")
            ins = SaleOrder.objects.get(id=self.kwargs['pk'])
            print( ins)
            if ins.delivered:
                ins.delivered = False
            else:
                # Subtract Stock
                instance_check = True
                if not ins.counted:
                    for item in ins.product.all():
                        product_item = Product.objects.get(name=item)
                        if product_item.stock_on_hand - item.quantity < 0:
                            messages.warning(self.request, f'Cannot deliver order, there are insufficient {product_item.name} products available')
                            instance_check = False
                        else:
                            product_item.stock_on_hand -= item.quantity
                            product_item.save()
                            instance_check = True
                            ins.counted = True
                ins.delivered = instance_check


            ins.save()
            return  redirect('transactions:sale-order-detail-view',self.kwargs['pk'])            
        else:
            return  redirect('transactions:sale-order-detail-view',self.kwargs['pk'])


# ============================================
# UPDATEVIEWS
    

# ===============================================================
#  CREATEVIEWS


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "transactions/form_items/product_create_form.html"
    success_url = reverse_lazy('transactions:new-product-form')


    def form_valid(self, form: ProductForm):
        name = form.cleaned_data['name']
        product_type = form.cleaned_data['product_type']
        
        product = Product.objects.filter(name=name, product_type = product_type)

        if product.exists():
            messages.warning(self.request, f'{name} ({product_type}) already exists, not added')

            return redirect('transactions:product-create-view')
             
        else:

            form.cleaned_data['stock_on_hand'] = 0
            form
            messages.success(self.request, f'{name} ({product_type}) successfully added')
            return super().form_valid(form)



class SaleOrderItemCreateView(LoginRequiredMixin, CreateView):
    model = SaleOrderItem
    template_name = "transactions/sale_order_item_create_view.html"
    success_url = reverse_lazy('transactions:sale-order-list-view')
    form_class = SaleOrderItemCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sales"] = SaleOrderItem.objects.filter(quantity__gt=0, ordered=False)
        return context
    
    def form_valid(self, form):
        clean_item = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']
        product_type = form.cleaned_data['product_type']

        item = SaleOrderItem.objects.filter(item=clean_item, ordered=False, product_type=product_type)
        if item.exists():
            gItem = SaleOrderItem.objects.get(item=clean_item, ordered=False,product_type=product_type)
            gItem.quantity += quantity 
            pricing_id = gItem.get_pricing(gItem.item.product_type,gItem.quantity)
            
            item.update(quantity=gItem.quantity, pricing = pricing_id )
            messages.success(self.request, f'{clean_item}  cart value has increased by {quantity}')
            return redirect('transactions:sale-order-item-create-view')

        else:
            
            SaleOrderItem.objects.create(item=clean_item, quantity=quantity,product_type=product_type)
            instance = SaleOrderItem.objects.filter(item=clean_item, ordered=False, quantity=quantity,product_type=product_type)
            gInstance = SaleOrderItem.objects.get(item=clean_item, ordered=False, quantity=quantity,product_type=product_type)

            pricing_id = SaleOrderItem.get_pricing(self,type=gInstance.product_type , moq=quantity)
            instance.update(pricing=pricing_id)

            messages.success(self.request, f'{clean_item}  successfully added to cart')
            return redirect('transactions:sale-order-item-create-view')
        
        


class SaleOrderCreateView(LoginRequiredMixin, CreateView):
    model = SaleOrder
    template_name = 'transactions/sale_order_create_view.html'
    form_class = SaleOrderCreateForm



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = SaleOrderItem.objects.filter(quantity__gt =0, ordered=False)
        context["sales"] = sales
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            

            logistics_company = form.cleaned_data['logistics_company']
            delivery_price = form.cleaned_data['delivery_price']
            customer = form.cleaned_data['customer']
            reference = "reference pending"
            instance = SaleOrder.objects.create(reference = reference,
                                      logistics_company=logistics_company,
                                      delivery_price=delivery_price,
                                      customer=customer
                                        )
            gSale = SaleOrder.objects.get(id=instance.id)
            fSale = SaleOrder.objects.filter(id=instance.id)
            oSale = SaleOrderItem.objects.filter(ordered=False,quantity__gt=0)

            for i in oSale:
                gSale.product.add(i)
                
            reference = SaleOrder.create_reference_number(gSale)
            oSale.update(sale_order_reference=reference, ordered=True)
            fSale.update(reference=reference)

        return redirect('transactions:sale-order-list-view')





# Third Party
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path




def render_pdf_view(request,*args,**kwargs):
    pk = kwargs.get('pk')
    sales_order = get_object_or_404(SaleOrder,id=pk)
    print(sales_order)
    template_path = 'transactions/invoice_template.html'
    context = {'object': sales_order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # To Download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # To Display:
    response['Content-Disposition'] = f'filename="{sales_order.reference}.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    print(html)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response






