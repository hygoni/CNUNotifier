import datetime
from rfeed import *
# year, month, date, hh, mm, ss
item1 = Item(
        title = "My 10 UNIX Command Line Mistakes",
        link = "https://www.cyberciti.biz/tips/my-10-unix-command-line-mistakes.html",
        description = "Here are a few mistakes that I made while working at UNIX/Linux prompt.",
    author = "Vivek Gite",
    guid = Guid("https://www.cyberciti.biz/tips/my-10-unix-command-line-mistakes.html"),
        pubDate = datetime.datetime(2017, 8, 1, 4, 0))
 
item2 = Item(
        title = "Top 25 Nginx Web Server Best Security Practices",
        link = "https://www.cyberciti.biz/tips/linux-unix-bsd-nginx-webserver-security.html",
        description = "Best Nginx web server hardening and security practice for Linux/Unix sysadmins and developers.",
    author = "Vivek Gite",
    guid = Guid("https://www.cyberciti.biz/tips/linux-unix-bsd-nginx-webserver-security.html"),
        pubDate = datetime.datetime(2017, 8, 1, 4, 2))
 
 
feed = Feed(
        title = "nixCraft Updated Tutorials/Posts",
        link = "https://www.cyberciti.biz/atom/updated.xml",
        description = "nixCraft Linux and Unix Sysadmin Blog - Recently updated posts",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = [item1, item2])
 
print(feed.rss())
