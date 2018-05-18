from .forms import ContactForm

def defaults(request):
    """ Returns the TMT API Version """
    return {
        'contact_form': ContactForm,
    }
