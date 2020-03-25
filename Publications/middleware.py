from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
import uuid


class SessionUidMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        if not request.session.get('uid'):
            request.session['uid'] = str(uuid.uuid4)
