from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from 'TimestampedModel' should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']


class UserLinkedModel(models.Model):
    user = models.CharField(max_length=255)

    class Meta:
        abstract = True


class TitleSlugDescriptionModel(models.Model):
    title = models.CharField(_('Title'), max_length=250)
    slug = models.SlugField(_('Slug'), unique=True)
    #description = models.TextField(verbose_name=_('Description'))
    description = RichTextField(verbose_name=_('Description'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    email = models.EmailField(_('Email'))
    message  = models.TextField(_('Message'))

    def __str__(self):
        return "%s (%s)" % (self.name, self.email)
