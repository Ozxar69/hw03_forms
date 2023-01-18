from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Страница об авторе."""
    template_name = 'app_name//about_author.html'


class AboutTechView(TemplateView):
    """Страница посвященная технолгии."""
    template_name = 'app_name//tech.html'
