import datetime
import requests
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse as dateutil_parse
from django.core.management.base import BaseCommand
from django.template.defaultfilters import striptags
from transcription.models import Transcript, Speaker, Statement


class Command(BaseCommand):

    speaker = Speaker.objects.get_or_create(
        first_name="Barack",
        last_name="Obama",
        party="d",
        display_name="Barack Obama"
    )

    legacy_classes = [
        (0, '.legacy-content p'),
        (1, '.legacy-para')
    ]

    def handle(self, *args, **options):

        self.get_transcripts()

    def get_transcripts(self):

        for transcript in Transcript.objects.all():
            soup = BeautifulSoup(transcript.full_text)

            print soup.select('p')




