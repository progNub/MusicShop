from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class StaffOrSuperuserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
