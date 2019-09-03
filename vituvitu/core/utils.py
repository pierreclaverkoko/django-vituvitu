import decimal
import json
import random
import string
import requests
from django.conf import settings
from django.contrib import messages

DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits
DEFAULT_CHAR_INTS = string.digits

MAXIMUM_SLUG_LENGTH = getattr(settings, "MAXIMUM_SLUG_LENGTH", 6)


ECONET_REGEX = r"^7[1269]{1}[0-9]{6}$"
SMART_REGEX = r"^7[5]{1}[0-9]{6}$"
LUMITEL_REGEX = r"^6[198]{1}[0-9]{6}$"
BDI_REGEX = r"^(?:[\+]|[0]{2})?(257)([0-9]{8})"


def complete_digit(digit, length=2):
    """
    A function to complete the left side of a INTEGER with '0' to fill the length desired
    Returns a CHAR.

    This is a copy of cbs.apps.core.utils.complete_digits
    """
    length = int(length)
    digit = int(digit)  # Convert To Int
    str_digit = "%s" % digit  # Convert To String in Order to have the Length
    digit_length = len(str_digit)

    if digit_length >= length:
        return str_digit
    else:
        i = 1
        while i <= (length - digit_length):
            str_digit = "0" + str_digit
            i = i + 1
        return str_digit


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return "".join(random.choice(chars) for _ in range(size))


def generate_random_ints(chars=DEFAULT_CHAR_INTS, size=6):
    return "".join(random.choice(chars) for _ in range(size))


def getornone(model, *args, **kwargs):
    """ sometime we want to get one or none object """
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return model.objects.none()


def send_sms_through_rapidpro(urns=[], text=""):
    """ This function sends messages through rapidpro.
    Contact(s) and the message to send to them must be in args json object.
    For example, your service could respond with the following JSON content
    to send a message to two contacts:
    Args:
    args (dict()): Json object containing the parameters as bellow.
    {
    "urns": ["tel:+2576543210", "tel:+25776543210"],
    "text": "Test"
    }
    Returns:
    Json
    """
    args = {"urns": list(urns), "text": text}
    url = getattr(settings, "RAPIDPRO_SEND_URL", "")
    token = getattr(settings, "RAPIDPRO_TOKEN", "")
    response = requests.post(
        url,
        headers={
            "Content-type": "application/json",
            "Authorization": "Token %s" % token,
        },
        data=json.dumps(args),
    )
    print(response.text)


def create_slug(slug):
    unique = generate_random_string()
    if not slug:
        slug = generate_random_string(size=30)

    if len(slug) > MAXIMUM_SLUG_LENGTH:
        slug = slug[:MAXIMUM_SLUG_LENGTH]

    while len(slug + "-" + unique) > MAXIMUM_SLUG_LENGTH:
        parts = slug.split("-")

        if len(parts) is 1:
            # The slug has no hypens. To append the unique string we must
            # arbitrarly remove `len(unique)` characters from the end of
            # `slug`. Subtract one to account for extra hyphen.
            slug = slug[: MAXIMUM_SLUG_LENGTH - len(unique) - 1]
        else:
            slug = "-".join(parts[:-1])

    return slug + "-" + unique


def pyexcel_function(pyexcel_obj, filename):
    file_data = pyexcel_obj.get_data(filename)
    print(json.dumps(file_data))
    return file_data


def read_excel_file(request, filename):
    file_data = False
    try:
        import pyexcel_xlsx as p

        file_data = pyexcel_function(p, filename)
    except AssertionError:
        pass

    if not file_data:
        try:
            import pyexcel_xls as p

            file_data = pyexcel_function(p, filename)
        except AssertionError:
            pass

    if not file_data:
        try:
            import pyexcel as p

            file_data = pyexcel_function(p, filename)
        except AssertionError:
            pass

    if not file_data:
        messages.error(
            request,
            "There was an error reading the File. Please check if the file extension is the one required and retry.",
        )
        messages.error(
            request, "If the error persists, please contact the administrator."
        )
    else:
        messages.success(request, "File Read Successfully.")
        return file_data
