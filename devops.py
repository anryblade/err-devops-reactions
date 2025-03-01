import random
try:
    from urllib import urlencode
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlencode, urljoin

from errbot import BotPlugin, botcmd

import requests
from pyquery import PyQuery


class DevOpsReactions(BotPlugin):

    @botcmd
    def devops(self, msg, args):
        """Return a gif based on search

        Return a random gif if no search query is specified.

        Example:
        !devops live migration
        !devops oops-wrong-cable
        !devops
        """

        base = 'https://devopsreactions.tumblr.com/'
        if args:
            q = urlencode({'q': args})
            path = '?' + q
        else:
            path = 'random'
        url = urljoin(base, path)
        r = requests.get(url)
        self.log.debug('url sent: {}'.format(r.url))

        if r.ok:
            dom = PyQuery(r.content)
            results = dom('figure[class=tmblr-full] img')
            self.log.debug('results found: {}'.format(len(results)))
        else:
            results = []

        if results:
            item = random.choice(results)
            return item.get('src')
#             return self.send_card(msg.frm,
#                            in_reply_to=msg,
#                            image=item.get('src'))
        else:
            return 'No results found.'
