from django.utils import timezone
from .models import DailyVisitor

class VisitorCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 세션이 없으면 생성합니다.
        if not request.session.session_key:
            request.session.create()

        today = timezone.now().date()
        session_key = request.session.session_key

        # 오늘 날짜의 방문 기록이 있는지 확인하고, 없으면 새로 만듭니다.
        visitor_record, created = DailyVisitor.objects.get_or_create(date=today)

        # 이 세션이 오늘 처음 방문한 경우에만 카운트를 1 증가시킵니다.
        if not request.session.get(f'visited_{today}', False):
            visitor_record.count += 1
            visitor_record.save()
            request.session[f'visited_{today}'] = True

        response = self.get_response(request)
        return response