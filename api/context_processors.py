from .models import UserTheme


def theme_context(request):
    current_theme = 'light'

    # Спочатку перевіряємо сесію (для всіх користувачів)
    current_theme = request.session.get('theme', 'light')

    # Потім перевіряємо базу даних (для авторизованих)
    if request.user.is_authenticated:
        try:
            # Спробуємо отримати PlatformUser
            if hasattr(request.user, 'platformuser'):
                user_theme, created = UserTheme.objects.get_or_create(
                    user=request.user.platformuser
                )
                current_theme = user_theme.theme
                # Синхронізуємо з сесією
                request.session['theme'] = current_theme
        except Exception as e:
            # У разі помилки використовуємо сесію
            current_theme = request.session.get('theme', 'light')

    return {'current_theme': current_theme}