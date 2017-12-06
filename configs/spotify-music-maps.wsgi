#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/spotify-music-maps/")

from run import app as application
application.secret_key = '\xe2\x1dy\xcc\xca\xdasl(\xc3KS\xd1c\xf5\xb8\xcdQ\x90wsF\x8a{'
