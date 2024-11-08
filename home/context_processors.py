from django.utils import timezone

def current_year(request):
    return {'year': timezone.now().year}