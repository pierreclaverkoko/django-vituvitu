from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
import requests

class CheckReCAPTCHAMixin(object):
    """
    Mixin for validating ReCaptcha

    must come Before `django-braces` 's FormMessagesMixin

    For Example:

    from django.utils.translation import ugettext_lazy as _
    from braces.views import FormMessagesMixin
    class RegistrationView(CheckReCAPTCHAMixin, FormMessagesMixin, CreateView):
        template_name = 'registration/register.html'
        model = User
        form_class = `YourRegistrationForm`

        success_url = `your_succes_url`
        form_invalid_message = _("Something went wrong, Registration aborted.")

        def get_form_valid_message(self):
            return _("You have been registered successfully.")

    """
    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            self.request.recaptcha_is_valid = True
            return super(CheckReCAPTCHAMixin, self).form_valid(form)
        else:
            self.request.recaptcha_is_valid = False
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return super(CheckReCAPTCHAMixin, self).form_invalid(form)


class UserFormKwargsMixin(object):
    """
    CBV mixin which puts the user from the request into the form kwargs.
    Note: Using this mixin requires you to pop the `user` kwarg
    out of the dict in the super of your form's `__init__`.
    """
    def get_form_kwargs(self, **kwargs):
        kwargs = super(UserFormKwargsMixin, self).get_form_kwargs(**kwargs)
        kwargs["user"] = self.request.user
        return kwargs

class PageHtmlMetaMixin(object):
    """
    Mixin allows you to set page HTML Meta Information

    page_meta_title
    page_meta_description
    page_meta_keyword
    page_meta_author
    """
    page_meta_title = ''
    page_meta_title_append = getattr(settings, 'PAGE_META_DEFAULT_TITLE_APPEND', '')
    page_meta_description = getattr(settings, 'PAGE_META_DEFAULT_DESCRIPTION', '')
    page_meta_keywords = None
    page_meta_author = getattr(settings, 'PAGE_META_DEFAULT_AUTHOR', '')
    page_id = ''

    def get_context_data(self, **kwargs):
        kwargs = super(PageHtmlMetaMixin, self).get_context_data(**kwargs)
        kwargs["page_meta_title"] = self.get_page_meta_title()
        kwargs["page_meta_title_append"] = self.page_meta_title_append
        kwargs["page_meta_description"] = self.get_page_meta_description()
        kwargs["page_meta_keywords"] = self.get_page_meta_keywords()
        kwargs["page_meta_author"] = self.get_page_meta_author()
        kwargs["page_id"] = self.page_id
        return kwargs

    def get_page_meta_keywords(self):
        if self.page_meta_keywords is None:
            s = ", "
            return s.join(getattr(settings, 'PAGE_META_DEFAULT_KEYWORDS', []))
        else:
            try:
                s = ", "
                k = getattr(settings, 'PAGE_META_DEFAULT_KEYWORDS', [])
                k.extend(self.page_meta_keywords)
                print(k)
                return s.join( k )
            except:
                return self.page_meta_keywords

    def get_page_meta_title(self):
        return self.page_meta_title

    def get_page_meta_description(self):
        return self.page_meta_description

    def get_page_meta_author(self):
        return self.page_meta_author


class TwoFactorMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (user.is_authenticated and "verified" in self.request.session)
