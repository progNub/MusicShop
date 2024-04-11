from django.http import HttpResponse
from card.models import Order


class UserIsOrderOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        if order_id:
            order = Order.objects.filter(id=order_id, user=request.user).first()
            if not order:
                return HttpResponse('У вас нет прав для выполнения этого действия.', status=403)
        return super().dispatch(request, *args, **kwargs)

