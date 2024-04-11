from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import JsonResponse

from card.forms import ChooseDeliverymanForm
from card.mixins import UserIsOrderOwnerMixin
from card.models import Order
from products.mixins import StaffOrSuperuserRequiredMixin


class OrderListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Order
    template_name = 'card/order_list.html'
    context_object_name = 'order_list'
    paginate_by = 10
    ordering = ('-date',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class AddProductToCartView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        print('AddProductToCartView')
        product_slug = request.POST.get('product_slug')
        quantity = request.POST.get('quantity', 1)
        if not product_slug:
            return HttpResponse('Товар не указан', status=400)

        # Здесь должна быть логика добавления товара в корзину
        # Например, add_to_cart(request, product_id, quantity)
        Order.add_product_to_cart(request.user, product_slug, quantity)

        # Перенаправление на страницу корзины или где вы хотите показать результат
        return redirect('orders')  # 'cart_detail_url' - это имя URL вашей страницы корзины


class RemoveProductToCartView(UserIsOrderOwnerMixin, View):

    def post(self, request, *args, **kwargs):
        print('RemoveProductToCartView')

        order_id = kwargs.get('order_id')
        if not order_id:
            return HttpResponse(f'id {order_id} заказа не передан.', status=400)
        try:
            Order.objects.get(id=order_id).delete()
        except Order.DoesNotExist:
            return HttpResponse(f'id {order_id} не существует.', status=400)

        # Перенаправление на страницу корзины
        return redirect('orders')


class UpdateProductQuantityInView(UserIsOrderOwnerMixin, View):

    def post(self, request, *args, **kwargs):

        print('UpdateProductQuantityInView')
        try:
            data = json.loads(request.body)  # Десериализация JSON тела запроса
            product_id = data.get('productId')  # Извлечение productId из данных запроса
            quantity = data.get('quantity')  # Извлечение quantity из данных запроса
            print(f'Product ID: {product_id}, Quantity: {quantity}')
            order = Order.objects.filter(product_id=product_id).first()

        except json.JSONDecodeError:
            return HttpResponse('Неверный формат JSON', status=400)

        except Exception as e:
            return HttpResponse(str(e), status=400)

        if quantity is not None and int(quantity) < 0:
            return JsonResponse({'status': 'error', 'message': 'Количество не может быть отрицательным'}, status=400)

        if order:
            print(order)
            new_quantity = order.set_quantity(quantity)
            return JsonResponse(
                {'status': 'success',
                 'message': 'Количество товара обновлено',
                 'new_quantity': new_quantity,
                 'new_price': order.total_price})


class ListOrderProductConfirmView(StaffOrSuperuserRequiredMixin, ListView):
    model = Order
    template_name = 'card/order_list_for_confirm.html'
    context_object_name = 'order_list'
    paginate_by = 10
    ordering = ('-date',)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(status='pending')
        return queryset


class ProcessingOrderView(StaffOrSuperuserRequiredMixin, UpdateView):
    model = Order
    template_name = 'card/processing_order.html'
    pk_url_kwarg = 'pk'
    form_class = ChooseDeliverymanForm
    context_object_name = 'order'
    success_url = reverse_lazy('orders')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'shipped'
        self.object.save()
        return super(ProcessingOrderView, self).form_valid(form)
