import datetime
import requests
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse as dateutil_parse
from django.core.management.base import BaseCommand
from django.template.defaultfilters import striptags
from transcription.models import Transcript, Speaker, Statement


class Command(BaseCommand):

    REMARKS_WORDS = [
        u'remarks',
        u'Remarks',
        u'REMARKS'
    ]


    legacy_classes = [
        (0, '.legacy-content p'),
        (1, '.legacy-para')
    ]

    PRESIDENT_WORDS = [
        u'PRESIDENT OBAMA:',
        u'THE PRESIDENT:'
    ]

    def handle(self, *args, **options):

        self.get_transcripts()

    def parse_remarks(self, transcript, soup):

        try:
            s = Speaker.objects.get(
                first_name="Barack",
                last_name="Obama",
                party="d",
                display_name="Barack Obama"
            )

        except:
            s = Speaker(
                first_name="Barack",
                last_name="Obama",
                party="d",
                display_name="Barack Obama"
            )
            s.save()

        transcript.location_text = soup.select('p.rtecenter')[0].get_text()
        president_speaking = False
        line_list = []
        for paragraph in soup.select('p'):

            if len(soup.select('p')) <= 6:

                if len(paragraph.select('br')) > 3:
                    line_list = paragraph\
                        .get_text()\
                        .replace(u'\xa0', '')\
                        .replace('\n\t\n', '\n')\
                        .split(u'\n')

            else:
                for paragraph in soup.select('p'):
                    line_list.append(u'%s' % paragraph.get_text())

        for line in line_list:
            for word in self.PRESIDENT_WORDS:

                if word in line:
                    president_speaking = True
                    line = line.replace(word, '')

                else:
                    if re.match("^[A-Z .]{2}[A-Z .]+: ", line.strip()):
                        president_speaking = False

            if president_speaking == True:
                if len(line.strip()) > 300:

                    try:
                        Statement.objects.get(
                            full_text=line.strip(),
                            speaker = s,
                            transcript=transcript)

                    except Statement.DoesNotExist:
                        st = Statement(
                                full_text=line.strip(),
                                length=len(line.strip()),
                                speaker = s,
                                transcript = transcript
                            )

                        s.save()
                        print st.speaker, st.length

        transcript.parsed = True
        transcript.save()


    def get_transcripts(self):

        for transcript in Transcript.objects.filter(parsed=False):
            soup = BeautifulSoup(transcript.full_text)

            for word in self.REMARKS_WORDS:
                if word in transcript.headline:
                    self.parse_remarks(transcript, soup)
