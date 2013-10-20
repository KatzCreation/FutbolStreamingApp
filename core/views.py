# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from bs4 import BeautifulSoup, SoupStrainer
import urllib2
from bs4.element import Tag, NavigableString
import re
from django.views.decorators.csrf import csrf_exempt, csrf_protect


def Soupify(url):
    response = urllib2.urlopen(url)
    source = response.read()
    soup = BeautifulSoup(source)
    return soup


def base(request, template="core/base.html"):
    return render_to_response(template)

@csrf_exempt
def scrape(request):
    print('hello')
    if request.is_ajax():
        base_url = "http://firstrowus1.eu/"
        soup = Soupify(base_url)
        team = request.POST.get('team', False)
        game_list = soup.find(id="accordion")
        games = "<br>"
        length = len(game_list.contents)
#        import pdb
#        pdb.set_trace()
        count = 0
        for i in range(0, length):
            if i % 4 == 1:
                game = game_list.contents[i]
                time = game.span.text.strip()
                name = game.text.strip()
                if re.search(team, name):
                    games += name + "<br>"
                    count += 1
#                    import pdb
#                    pdb.set_trace()
                    links = game_list.contents[i+2]
                    num_links = len(links.contents)
                    for j in range(5, num_links):
                        link = links.contents[j]
                        if type(link) == Tag:
                            if link.has_attr('href'):
                                num = (j - 3) / 2
                                games += "<a href='" + "http://firstrowus1.eu/" + link['href'] + "' target='_blank'>Link " + str(num) + "</a></br>"

        if not count:
            games += "Sorry, They arent playing any games soon"
        return HttpResponse(games)
    else:
        return HttpResponse('error')

