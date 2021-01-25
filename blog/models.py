from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    # content_panels = Page.content_panels + [
    #     FieldPanel('intro', classname="full")
    # ]
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)  # Retrieve the original context
        blogpages = self.get_children().live().order_by('-first_published_at')  # Reorder
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),

        # This makes the gallery images available on the editing interface for BlogPage
        InlinePanel('gallery_images', label="Gallery images"),
    ]


# Inheriting from Orderable adds a sort_order field to the model to keep track of the ordering of images in the gallery
class BlogPageGalleryImage(Orderable):

    """
    The ParentalKey to BlogPage is what attaches the gallery images to a specific page. It works similar to a ForeignKey, but also defines BlogPageGalleryImage as a "child" of the BLogPage model, so that it's treated as a fundamental part of the page in operations like submitting for moderation and tracking revision history.
    """
    page = ParentalKey(BlogPage, on_delete=models.CASCADE,
                       related_name="gallery_images")

    '''
    images is a ForeignKey to Wagtail's build-in Image model, where the images themselves are stored. This comes with a dedicated panel type, ImageChooserPanel, which provides a pop-up interface for choosing an existing image or uploading a new one. This way, we allow an image to exist in multiple galleries - effectively, we've created a many-to-many relationship between pages and images.
    '''
    image = models.ForeignKey(
        '''
        Specifying on_delete=models.CASCADE on the foreigm key means that if the image is deleted from the system, the gallery entry is deleted as well. If we want to leave the entry in place, we'd set the foreign key diff -- on_delete=models.SET_NULL
        '''
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        # Being imported with the argument from line 47
        ImageChooserPanel('image'),
        FieldPanel('caption')  # Being imported with the argument from line 50
    ]
