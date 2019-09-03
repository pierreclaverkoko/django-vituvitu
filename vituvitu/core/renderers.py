import json
import decimal

from rest_framework.renderers import JSONRenderer


class ExtendedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        # print("TTTTTTTTTTYYYYYYYYYYYYYYPPPPPPPPPPEEEEEE : ", obj, type(obj))
        # Let the base class default method raise the TypeError
        return super(ExtendedEncoder, self).default(obj)


class ConduitJSONRenderer(JSONRenderer):
    """
    From the Conduit App tutorial  on Thinkster.
    """

    charset = "utf-8"
    object_label = "object"
    pagination_object_label = "objects"
    pagination_object_count = "count"

    def render(self, data, media_type=None, renderer_context=None):
        if getattr(data, "get", None):
            if data.get("results", None) is not None:
                return json.dumps(
                    {
                        self.pagination_object_label: data["results"],
                        self.pagination_count_label: data["count"],
                    },
                    cls=ExtendedEncoder,
                )

            # If the view throws an error (such as the user can't be authenticated
            # or something similar), `data` will contain an `errors` key. We want
            # the default JSONRenderer to handle rendering errors, so we need to
            # check for this case.
            elif data.get("errors", None) is not None:
                return super(ConduitJSONRenderer, self).render(data)

        return json.dumps({self.object_label: data}, cls=ExtendedEncoder)
