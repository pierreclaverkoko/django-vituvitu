from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

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
        recaptcha_response = self.request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()
        if result["success"]:
            self.request.recaptcha_is_valid = True
            return super(CheckReCAPTCHAMixin, self).form_valid(form)
        else:
            self.request.recaptcha_is_valid = False
            messages.error(self.request, "Invalid reCAPTCHA. Please try again.")
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

    page_meta_title = ""
    page_meta_title_append = getattr(settings, "PAGE_META_DEFAULT_TITLE_APPEND", "")
    page_meta_description = getattr(settings, "PAGE_META_DEFAULT_DESCRIPTION", "")
    page_meta_keywords = None
    page_meta_author = getattr(settings, "PAGE_META_DEFAULT_AUTHOR", "")
    page_id = ""

    def get_context_data(self, *args, **kwargs):
        context = super(PageHtmlMetaMixin, self).get_context_data(*args, **kwargs)
        context["page_meta_title"] = self.get_page_meta_title()
        context["page_meta_title_append"] = self.page_meta_title_append
        context["page_meta_description"] = self.get_page_meta_description()
        context["page_meta_keywords"] = self.get_page_meta_keywords()
        context["page_meta_author"] = self.get_page_meta_author()
        context["page_id"] = self.page_id
        return context

    def get_page_meta_keywords(self):
        if self.page_meta_keywords is None:
            s = ", "
            return s.join(getattr(settings, "PAGE_META_DEFAULT_KEYWORDS", []))
        else:
            try:
                s = ", "
                k = getattr(settings, "PAGE_META_DEFAULT_KEYWORDS", [])
                k.extend(self.page_meta_keywords)
                # print(k)
                return s.join(k)
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
        return user.is_authenticated and "verified" in self.request.session


class EnsureCsrfCookieMixin(object):
    """
    Ensures that the CSRF cookie will be passed to the client.
    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCsrfCookieMixin, self).dispatch(*args, **kwargs)


class PaginationMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        paginate_by = self.get_paginate_by(queryset)
        page_q = self.paginate_queryset(queryset, self.get_paginate_by(queryset))
        begin_pages = 5
        end_pages = 5
        before_pages = 5
        after_pages = 5
        page = page_q[1]
        get_string = ""
        for key, value in self.request.GET.items():
            if key != "page":
                get_string += "&%s=%s" % (key, value)

        page_range = list(page.paginator.page_range)
        begin = page_range[:begin_pages]
        end = page_range[-end_pages:]
        middle = page_range[
            max(page.number - before_pages - 1, 0) : page.number + after_pages
        ]

        if set(begin) & set(middle):  # [1, 2, 3], [2, 3, 4], [...]
            begin = sorted(set(begin + middle))  # [1, 2, 3, 4]
            middle = []
        elif begin[-1] + 1 == middle[0]:  # [1, 2, 3], [4, 5, 6], [...]
            begin += middle  # [1, 2, 3, 4, 5, 6]
            middle = []
        elif middle[-1] + 1 == end[0]:  # [...], [15, 16, 17], [18, 19, 20]
            end = middle + end  # [15, 16, 17, 18, 19, 20]
            middle = []
        elif set(middle) & set(end):  # [...], [17, 18, 19], [18, 19, 20]
            end = sorted(set(middle + end))  # [17, 18, 19, 20]
            middle = []

        if set(begin) & set(end):  # [1, 2, 3], [...], [2, 3, 4]
            begin = sorted(set(begin + end))  # [1, 2, 3, 4]
            middle, end = [], []
        elif begin[-1] + 1 == end[0]:  # [1, 2, 3], [...], [4, 5, 6]
            begin += end  # [1, 2, 3, 4, 5, 6]
            middle, end = [], []

        context["page_range"], context["begin"], context["end"], context["middle"] = (
            page_range,
            begin,
            end,
            middle,
        )

        print(context)

        return context
