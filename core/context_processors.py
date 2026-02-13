from django.utils import timezone

def current_time(request):
    """
    This makes the variable 'now' available in every 
    template without adding it to the view context.
    """
    return {
        'now': timezone.now()
    }