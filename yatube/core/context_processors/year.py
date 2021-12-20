from django.utils import timezone


def year(request):
    """Добавляет в контекст переменную greeting с приветствием."""

    return {
        'greeting': 'Халлё',
        'year': timezone.now().year,
    }
