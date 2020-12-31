from .models import UserRequestCount
from django.utils.deprecation import MiddlewareMixin
from rest_framework_jwt import authentication
from django.db.models import Sum


class ServerRequestCountMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            count = list(UserRequestCount.objects.annotate(count=Sum('request_count')).values_list('count', flat=True))
            if count and count[0] > 100:
                count_obj = UserRequestCount.objects.all().delete()

            request.user = authentication.JSONWebTokenAuthentication().authenticate(request)[0]
            request_count = UserRequestCount.objects.filter(user_id=request.user.id).first()
            if request_count:
                request_count.request_count += 1
                request_count.save()
            else:
                request_count = UserRequestCount.objects.create(user_id=request.user.id,
                                                                request_count=1)
            return None
        except:
            pass
