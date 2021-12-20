from django.views.generic.base import TemplateView


class StaticPageAuthor(TemplateView):
    template_name = 'about/author.html'


class StaticPageTech(TemplateView):
    template_name = 'about/tech.html'
