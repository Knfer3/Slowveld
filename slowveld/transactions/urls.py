
from django.urls import path
from .views import (
    # Form
    SlowveldFormsView,
    PurchaseItemFormView,
    PurchaseOrderFormView,
    NewProductFormView,
    ProductFormView,

    # List
    PurchaseOrderListView,
    ItemsListView,
    StockListView,
    ProductListView,
    SaleOrderListView,

    # Detail
    ItemsDetailView,
    PurchaseOrderDetailview,
    SaleOrderDetailView,

    # Update
    ProductUpdateView,

    # Create
    ProductCreateView,
    SaleOrderItemCreateView,
    SaleOrderCreateView,


    # Third party
    render_pdf_view,
)

app_name = 'transactions'

urlpatterns = [
    
    
    # Forms 
    path('forms/', SlowveldFormsView.as_view(), name='slowveld-forms'),
    path('forms/purchase-item/', PurchaseItemFormView.as_view(), name='purchase-item-form'),
    path('forms/purchase-order/', PurchaseOrderFormView.as_view(), name='purchase-order-form'),
    path('forms/new-product/', NewProductFormView.as_view(), name='new-product-form'),
    path('forms/product', ProductFormView.as_view(),name='product-form'),
    path('forms/product/create',ProductUpdateView.as_view(),name='product-update-form' ),


    # ListViews
    path('list/purchase-orders/', PurchaseOrderListView.as_view(),name='purchase-order-list-view'),
    path('list/items/', ItemsListView.as_view(), name='items-list-view'),
    path('list/stock/', StockListView.as_view(), name='stock-list-view'),
    path('list/Products/', ProductListView.as_view(), name='product-list-view'),
    path('list/sales/', SaleOrderListView.as_view(), name='sale-order-list-view'),



    # DetailViews
    path('detail/<int:pk>/', ItemsDetailView.as_view(),name='items-detail-view'),
    path('detail/order/<int:pk>/',PurchaseOrderDetailview.as_view(),name='order-detail-view' ),
    path('detail/sale/order/<int:pk>/', SaleOrderDetailView.as_view(), name='sale-order-detail-view'),


    # UpdateViews


    # CreateView
    path('create/product/', ProductCreateView.as_view(), name='product-create-view'),
    path('create/sale/item/', SaleOrderItemCreateView.as_view(),name='sale-order-item-create-view'),
    path('create/sale/order/', SaleOrderCreateView.as_view(),name='sale-order-create-view'),


    # Third party
    path('detail/sale/order/<int:pk>/pdf/', render_pdf_view, name='sale-order-generate-pdf'),
]