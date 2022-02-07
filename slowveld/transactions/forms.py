from django import forms
from .models import Item, PurchaseOrder, NewProduct, Product, SaleOrderItem, SaleOrder
from apps.utils.models import Type

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ['slug', 'uom_quantity_purchased']

    def __init__(self, *args, **kwargs):
        super(PurchaseItemForm, self).__init__(*args, **kwargs)

        self.fields['item'].widget.attrs.update({
                                            'name':'item_form',
                                            'type':'text',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Item interested in purchasing',
                                            })
        self.fields['description'].widget.attrs.update({
                                             'name':'item_form',
                                             'type':'text',
                                             'class':'form-control has-feedback-left',
                                             'rows':'3', 
                                             'cols':'5',
                                             'placeholder':'Description'
                                             })


        self.fields['category'].empty_label = "Category"
        self.fields['category'].widget.attrs.update({
                                             'name':'item_form',
                                             'class':'form-control has-feedback-left',
                                             "empty_label":"Select",
                                             'label':"",
                                             })
        self.fields['cost_price'].widget.attrs.update({
                                            'name':'item_form',
                                            'type':'text',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Price of the item',
                                            })
        self.fields['uom_quantity'].widget.attrs.update({
                                            'name':'item_form',
                                            'type':'text',
                                               'class': 'form-control has-feedback-left',
                                            'placeholder':'UOM quantity',
                                            })
        self.fields['uom'].empty_label = "UOM"
        self.fields['uom'].widget.attrs.update({
                                             'name':'item_form',
                                             'class':'form-control',
                                             "empty_label":"Select",
                                             'label':"",
                                             })     
        self.fields['sold_in_packs'].widget.attrs.update({
                                        'name':'item_form',
                                        'type':'checkbox',
                                        'class': 'flat',
                                        'label':'MOQ',
                                        })                                       
        

class ItemCartForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ['item','description','category','uom_quantity','uom','cost_price','slug']

    def __init__(self, *args, **kwargs):
        super(ItemCartForm, self).__init__(*args, **kwargs)

        self.fields['uom_quantity_purchased'].widget.attrs.update({
                                            'name':'item_cart_form',
                                            'type':'int',
                                               'class': 'form-control has-feedback-left',
                                            'placeholder':'Quantity',
                                            })


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        exclude = ['status','received','order_cost']

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)

        self.fields['purchase_order_reference'].widget.attrs.update({
                                            'name':'Purchase_Order_Form',
                                            'type':'text',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Order reference',
                                            })
        self.fields['delivery_price'].widget.attrs.update({
                                            'name':'Purchase_Order_Form',
                                            'type':'decimal',
                                               'class': 'form-control has-feedback-left',
                                            'placeholder':'Delivery cost',
                                            })

        self.fields['supplier'].empty_label = "Supplier"
        self.fields['supplier'].widget.attrs.update({
                                             'name':'item_form',
                                             'class':'form-control has-feedback-left',
                                             "empty_label":"Select",
                                             'label':"",
                                             })


class NewProductForm(forms.ModelForm):
    class Meta:
        model = NewProduct
        fields = "__all__"
        exclude = ('product_type', 'description')


    def __init__(self, *args, **kwargs):
        super(NewProductForm, self).__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({
                                            'name':'new_product',
                                            'type':'text',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'New product name',
                                            })
                                  

        self.fields['input_item'].empty_label = "Item"
        self.fields['input_item'].widget.attrs.update({
                                             'name':'new_product',
                                             'class':'form-control has-feedback-left',
                                             "empty_label":"Select",
                                             'label':"",
                                             })
        self.fields['input_quantity'].widget.attrs.update({
                                            'name':'new_product',
                                            'type':'decimal',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'quantity per product',
                                            })



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["slug","image", 'reserve_quantity', 'stock_on_hand',]



    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
                                            'name':'product',
                                            'type':'text',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Product name',
                                            })
        self.fields['description'].widget.attrs.update({
                                             'name':'product',
                                             'type':'text',
                                             'class':'form-control has-feedback-left',
                                             'rows':'3', 
                                             'cols':'5',
                                             'placeholder':'Description'
                                             })
        self.fields['product_type'].empty_label = "Type"
        self.fields['product_type'].widget.attrs.update({
                                             'name':'product',
                                             'class':'form-control has-feedback-left',
                                             "empty_label":"Select",
                                             'label':"",
                                             })             


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['inputs','description','slug','image','product_type']


    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.ModelChoiceField(queryset=Product.objects.all())
        self.fields['name'].widget.attrs.update({
                                            'name':'product',
                                            'type':'select',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'product name',
                                            })
        self.fields['stock_on_hand'].widget.attrs.update({
                                            'name':'product',
                                            'type':'int',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Quantity created',
                                            }) 
                                            
class PurchaseOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        exclude = ['purchase_order_reference','item','supplier','delivery_price','order_cost',]                              


class SaleOrderItemCreateForm(forms.ModelForm):
    class Meta:
        model = SaleOrderItem
        fields = "__all__"
        exclude = ['delivered','ordered', 'pricing']   

    def __init__(self, *args, **kwargs):
        super(SaleOrderItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['product_type'] = forms.ModelChoiceField(queryset=Type.objects.all())
        self.fields['product_type'].widget.attrs.update({
                                            'name':'SalesOrderItem',
                                            'type':'select',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Product type',
                                            })
        self.fields['item'].widget.attrs.update({
                                            'name':'SalesOrderItem',
                                            'type':'select',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Product name',
                                            })
        self.fields['quantity'].widget.attrs.update({
                                            'name':'product',
                                            'type':'int',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Number of products',
                                            }) 

class SaleOrderCreateForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = "__all__"
        exclude = ['reference','product','quantity','status']   

    def __init__(self, *args, **kwargs):
        super(SaleOrderCreateForm, self).__init__(*args, **kwargs)

        self.fields['customer'].widget.attrs.update({
                                            'name':'SalesOrderItem',
                                            'type':'select',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Product name',
                                            })
        self.fields['delivery_price'].widget.attrs.update({
                                            'name':'product',
                                            'type':'int',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Delivery price',
                                            }) 
        self.fields['logistics_company'].widget.attrs.update({
                                            'name':'SalesOrderItem',
                                            'type':'select',
                                            'class': 'form-control has-feedback-left',
                                            'placeholder':'Product name',
                                            })

        self.fields['proof_of_payment'].widget.attrs.update({
                                        'name':'item_form',
                                        'type':'checkbox',
                                        'class': 'flat',
                                        'label':'MOQ',
                                        }) 





