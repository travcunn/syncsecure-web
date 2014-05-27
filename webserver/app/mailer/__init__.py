import time

import mandrill


mandrill_client = mandrill.Mandrill('t6vt9a6i1IQbTBOUhGIItA')

message_template = {'auto_html': None,
                    'auto_text': None,
                    'from_email': 'support@syncsecure.com',
                    'from_name': 'SyncSecure Support',
                    'google_analytics_campaign': 'support@syncsecure.com',
                    'google_analytics_domains': ['syncsecure.com'],
                    'headers': {'Reply-To': 'support@syncsecure.com'},
                    'html': '<p>Example HTML content</p>',
                    'important': False,
                    'inline_css': True,
                    'metadata': {'website': 'syncsecure.com'},
                    'preserve_recipients': True,
                    'recipient_metadata': [{'rcpt': 'recipient.email@example.com',
                                            'values': {'user_id': 123456}}],
                    'return_path_domain': None,
                    'signing_domain': 'syncsecure.com',
                    'subject': 'example subject',
                    'tags': ['password-resets'],
                    'text': 'Example text content',
                    'to': [{'email': 'travcunn@umail.iu.edu',
                            'name': 'Recipient Name',
                            'type': 'to'}],
                    'track_clicks': False,
                    'track_opens': False,
                    'tracking_domain': None,
                    'url_strip_qs': False,
                    'view_content_link': None}


class Mailer(object):
    def __init__(self, mandrill_client):
        self.__m = mandrill_client

    def test_mail(self, recipient):
        try:
            result = self.__m.messages.send(message=message_template,
                                            async=True)
        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise

        return result
