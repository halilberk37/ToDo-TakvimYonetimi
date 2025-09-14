from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(TemplateView):
    """
    Ana sayfa view'ı
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TodoCalendar - Ana Sayfa'
        return context


@login_required
def dashboard_view(request):
    """
    Dashboard view'ı (giriş yapmış kullanıcılar için)
    """
    context = {
        'title': 'Dashboard',
        'user': request.user,
    }
    return render(request, 'index.html', context)


def api_info_view(request):
    """
    API bilgilerini döndüren view
    """
    api_info = {
        'authentication': {
            'login': '/api/auth/login/',
            'register': '/api/auth/register/',
            'logout': '/api/auth/logout/',
            'profile': '/api/auth/profile/',
            'token_refresh': '/api/auth/token/refresh/',
        },
        'todos': {
            'list': '/api/todos/',
            'create': '/api/todos/',
            'detail': '/api/todos/{id}/',
            'update': '/api/todos/{id}/',
            'delete': '/api/todos/{id}/',
            'toggle': '/api/todos/{id}/toggle/',
            'statistics': '/api/todos/statistics/',
        },
        'calendar': {
            'calendars': '/api/calendar/calendars/',
            'events': '/api/calendar/events/',
            'today_events': '/api/calendar/events/today/',
            'upcoming_events': '/api/calendar/events/upcoming/',
            'statistics': '/api/calendar/statistics/',
        }
    }
    
    return JsonResponse(api_info) 