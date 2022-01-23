from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy

import datetime

class Index(TemplateView):
    """ This is the public index page. The index is always a public page """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        return context