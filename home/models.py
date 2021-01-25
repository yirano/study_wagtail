from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    # body is defined as a RichTextField -- you can use any of the Django core fields.
    body = RichTextField(blank=True)

    '''
    content_panels define the capabilities and the layout of the editing interface. (https://docs.wagtail.io/en/stable/topics/pages.html)
    '''
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]
