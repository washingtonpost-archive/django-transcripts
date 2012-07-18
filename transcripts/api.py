import datetime
import requests
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse as dateutil_parse
from django.core.management.base import BaseCommand
from django.template.defaultfilters import striptags
from transcripts.models import Transcript, Speaker, Statement


class Command(BaseCommand):

    base_url = 'http://www.whitehouse.gov/briefing-room/Speeches-and-Remarks/'
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
        self.get_statements()
        self.categorize_statements()

    def parse_transcript(self, link_url, headline):

        request = requests.get(link_url)
        soup = BeautifulSoup(request.content)

        if len(soup.select('.date')) > 0:
            return {
                'speaker': self.speaker,
                'date': dateutil_parse(soup.select('.date')[0]),
                'full_text': str(soup.select('.content'))
                'headline': headline,
                'url': link_url
            }
        else:
            return None



    def get_transcripts(self):
        years = range(2009, int(datetime.datetime.now().year) + 1)
        months = range(1, 13)

        for year in years:
            for month in months:
                if year == int(datetime.datetime.now().year):
                    if month <= int(datetime.datetime.now().month):
                        url = self.base_url + u'%s/%s' % (year, str(month).zfill(2))
                        request = requests.get(url)
                        soup = BeautifulSoup(request.content)

                        pages = range(0, len(soup.select('li.pager_item') + 2))

                        for page in pages:
                            request = requests.get(url + u'?page=%s' % page)
                            soup = BeautifulSoup(request.content)

                            speech_links = soup.select(
                                '#content ul.entry-list li.views-row a')

                            for link in speech_links:
                                presidential_speech = False
                                for word in self.PRESIDENT_WORDS:
                                    if word in link.get_text():
                                        presidential_speech = True

                                if presidential_speech == True:
                                    transcript_dict = self.parse_transcript(
                                        link.attrs['href'], link.get_text())
                                    print transcript_dict
                                    presidential_speech = False
