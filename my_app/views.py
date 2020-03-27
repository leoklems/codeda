import  requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import  BeautifulSoup
from . import models

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/sss?query={}'

def home(request):

    return  render(request, 'my_app/base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    # print(quote_plus(search))
    # quote_plus formats the content of the search  with plus signs and the requirements for use as valid part of a url
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # this concartinates the base url and the quote_plus formatted content of the search
    response = requests.get(final_url)
    data = response.text
    print(final_url)
    # print(data)
    soup = BeautifulSoup(data, features = 'html.parser')

    # this creates a beautiful soup object o fthe data variable as a html
    post_listings = soup.find_all('li',{'class': 'result-row'})

    final_postings  = []
    for post in post_listings:
        post_title = post.find(class_ = 'result-title').text
        post_url = post.find('a').get('href')

        if  post.find(class_ = 'result-price'):
            post_price = post.find(class_ = 'result-price').text

        else:
            new_response = requests.get(post_url)
            new_data = new_response.text
            new_soup = BeautifulSoup(new_data, features='html.parser')
            post_text = new_soup.find(id='postingbody').text

            rl = requests.findall(r'\$\w+', post_text)
            if rl :
                post_price = rl[0]
            else:
                post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            # post_image_id = post.find(class_='result-image').get('data-ids').split(',')[:]
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = "https://images.craigslist.org/{}_300x300.jpg". format(post_image_id)

        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"

        final_postings.append((post_title, post_url, post_price, post_image_url))

    print(final_postings)
    stuff_for_frontend =  {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)