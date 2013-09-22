#!python
# encoding=utf-8

import os
import sys
import re
import urllib
import urllib2
import cookielib
import httplib
import cgi
from optparse import OptionParser
from progressbar import *

# Constants for niconico
VIDEO_URL_FORMAT = "http://www.nicovideo.jp/watch/{video_id}"
LOGIN_URL = "https://secure.nicovideo.jp/secure/login"
API_URL = "http://flapi.nicovideo.jp/api/getflv/"
VIDEO_URL_RE = re.compile(r"http://www.nicovideo.jp/watch/([sn][mo]\d+)$")
VIDEO_TITLE_RE = re.compile(r'<h1><a class="video" [^<>]*>(.*)</a></h1>')

# Constants for progress bar
PBAR_WIDGETS = [Percentage(), " ", Bar(marker="=",left="[",right="]"),
           " ", ETA(), " ", FileTransferSpeed()]

COOKIE_FILE = "nico-cookie.txt"

class LoginError(Exception):
    pass

def login(mail, password):
    for i in range(2):
        if mail is None: mail = raw_input("mail: ")
        if password is None: password = raw_input("pass: ")
        query = {"mail":mail, "password":password}
        query = urllib.urlencode(query)
        try:
            response = urllib2.urlopen(LOGIN_URL, query)
            if response.headers["x-niconico-authflag"] == "1":
                return True
            else:
                mail = password = None
        except urllib2.URLError:
            pass
    return False

def get_flv_url(video_id):
    response = urllib2.urlopen(API_URL + video_id)
    try:
        content = response.read()
        flv_url = cgi.parse_qs(content)["url"][0]
        return flv_url
    except KeyError:
        if content == "closed=1&done=true":
            raise LoginError
        else:
            raise ValueError

def get_video_title(video_url):
    response = urllib2.urlopen(video_url)
    match = VIDEO_TITLE_RE.search(response.read())
    if match:
        video_title = match.group(1).decode("utf-8", "ignore")
        video_title = re.compile(u'[\/:*?"<>|]').sub(" ", video_title)
        return video_title

def download(flv_url, filepath):
    try:
        file = None
        response = urllib2.urlopen(flv_url)
        try:
            file = open(filepath, "wb")
        except IOError:
            raise RuntimeError("unable to open the file for writing")
        total = response.headers["content-length"]
        downloaded = 0
        pbar = ProgressBar(widgets=PBAR_WIDGETS, maxval=int(total)).start()
        while True:
            data = response.read(4096)
            if not data: break
            file.write(data)
            downloaded += len(data)
            pbar.update(downloaded)
        pbar.finish()
    except (urllib2.URLError, IOError):
        raise RuntimeError("unable to download video data")
    finally:
        if file: file.close()

# Create the command line options parser and parse command line
usage = "usage: %prog [options] http://www.nicovideo.jp/watch/{video_id}"
parser = OptionParser(usage)
parser.add_option("-m", dest="mail",
                  help="specify the email address")
parser.add_option("-p", dest="password",
                  metavar="PASS",
                  help="specify the password")
parser.add_option("-c", dest="cookie_file",
                  metavar="FILE",
                  help="load cookies from FILE of the Mozilla/Netscape 'cookie.txt' format"),
parser.add_option("-d", dest="save_dir",
                  metavar="PREFIX",
                  help="save a file to PREFIX/ (default current directory)")
parser.add_option("-n", dest="no_title",
                  action="store_true",
                  help="save the file under the name {ID}.flv (default {title}.flv)")

(options, args) = parser.parse_args()

# Check arguments
if not args:
    parser.print_help()
    sys.exit(1)
video_url = args[0]
match = VIDEO_URL_RE.match(video_url)
if match is None:
    sys.exit("Error: video url not in this format: %s" % VIDEO_URL_FORMAT)
video_id = match.group(1)

# Check whether the directory specified by -d option exists
if options.save_dir:
    if not os.path.isdir(options.save_dir):
        sys.exit("Error: %s is not a directory" % options.save_dir)

# Configure urllib2 to use cookies
cj = cookielib.MozillaCookieJar()
try:
    cj.load(options.cookie_file or COOKIE_FILE)
except:
    pass
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

# Prepare downloading video
try:
    try:
        flv_url = get_flv_url(video_id)
    except ValueError, e:
        sys.exit("Error: invalid video ID")
    except LoginError:
        # Exit if use the browser's cookies file
        if options.cookie_file:
            sys.exit("Error: not logged in")
        # Login and retry
        if login(options.mail, options.password):
            cj.save(COOKIE_FILE)
            flv_url = get_flv_url(video_id)
        else:
            sys.exit("Error: unable to login")
    video_title = get_video_title(video_url)      
except urllib2.URLError, e:
    sys.exit("Error: unable to prepare downloading a video")

# Download video
filename = video_title or video_id
if options.no_title:
    filename = video_id
filepath = os.path.join(options.save_dir or ".", filename + ".flv")
print video_title
try:
    download(flv_url, filepath)
except (IOError, RuntimeError), e:
    sys.exit("Error: %s" % e)
except httplib.BadStatusLine:
    sys.exit("Error: download seems to be limited")
