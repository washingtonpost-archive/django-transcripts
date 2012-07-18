from django.db import models

PARTY_CHOICES = (
    ('r', 'Republican'),
    ('d', 'Democrat'),
    ('i', 'Independent'),
)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        abstract = True


class Speaker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    party = models.CharField(max_length=5,
        choices=PARTY_CHOICES,
        blank=True,
        null=True)
    slug = models.SlugField(max_length=255)
    display_name = models.CharField(max_length=255)
    statement_count = models.IntegerField(default=0)

    class Meta:
        abstract = True

class Transcript(models.Model):
    """Examples of the kind of model code you'd want to tie these together.
    speakers = models.ManyToManyField(Speaker, blank=True, null=True)
    """
    date = models.DateField()
    full_text = models.TextField()
    headline = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    transcript_type = models.CharField(max_length=255)
    location_text = models.TextField(blank=True, null=True)
    parsed = models.BooleanField(default=False)
    parsed_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Statement(models.Model):
    """Examples of the kind of model code you'd want to tie these together.
    speaker = models.ForeignKey(
        Speaker,
        related_name='speaker')
    target = models.ForeignKey(
        Speaker,
        related_name='target',
        blank=True,
        null=True)
    transcript = models.ForeignKey(Transcript)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    """
    full_text = models.TextField()
    length = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    parsed = models.BooleanField(default=False)
    parsed_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
