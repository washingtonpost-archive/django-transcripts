from django.db import models
from django.template.defaultfilters import slugify

PARTY_CHOICES = (
    ('r', 'Republican'),
    ('d', 'Democrat'),
    ('i', 'Independent'),
)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__unicode__())
        super(Category, self).save(*args, **kwargs)


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

    def __unicode__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = u'%s %s' % (self.first_name, self.last_name)
        self.slug = slugify(self.__unicode__())


class Transcript(models.Model):
    date = models.DateField()
    full_text = models.TextField()
    headline = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    transcript_type = models.CharField(max_length=255)
    location_text = models.TextField(blank=True, null=True)
    parsed = models.BooleanField(default=False)
    parsed_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    speakers = models.ManyToManyField(Speaker, blank=True, null=True)

    def __unicode__(self):
        if len(self.speakers_set.all()) > 0:
            speaker_text = ", ".join(
                [s.display_name for s in self.speakers.all()])
            return u'%s: %s' % (self.date, speaker_text)
        else:
            return u'%s: %s' % (self.date, self.location_text)


class Statement(models.Model):
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
    full_text = models.TextField()
    length = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    parsed = models.BooleanField(default=False)
    parsed_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s: %s (%s)' % (
            self.transcript.date,
            self.speaker,
            self.length)
