from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages

import json

from django.contrib.messages.views import SuccessMessageMixin

import datetime

from PIL import Image
import PIL.ExifTags

from imglibrary.models import ImageFile
from .forms import FrmImageUpload

class Index(SuccessMessageMixin, CreateView):
    """ This is the public index page. The index is always a public page """
    template_name = "index.html"
    form_class = FrmImageUpload
    model = ImageFile
    success_message = "Successfully uploaded image!"

    def form_valid(self,form):
        print("\n\n\t=>Inside Index::form_valid ...")
        context = self.get_context_data(form=form)

        self.object = form.save()

        messages.success(self.request, 'Successfully uploaded image!')
        return HttpResponseRedirect(reverse_lazy('imglibrary:view-image',args=[self.object.id]))
    
    def form_invalid(self, form):
        print("inside Index.form_invalid")
        print("*** Printing form errors ***")
        print(form.errors)

        data = {'upload_status_is_success':False}
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        return context