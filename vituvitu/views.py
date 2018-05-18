from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.views import View
from .core.mixins import PageHtmlMetaMixin
from .models import Contact
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

def contact_success(request):
    """ Contact Success Page """
    page_title = "contact"
    return render(request, 'base/contact_success.html', locals())


class ContactCreate(PageHtmlMetaMixin, CreateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('contact_success')
    page_meta_title = _('Contact')
    page_id = 'Contact'
    template_name = 'base/contact_form.html'

    def get_context_data(self, **kwargs):
        context = super(ContactCreate, self).get_context_data(**kwargs)
        context['page_title'] = 'contact'

        return context

