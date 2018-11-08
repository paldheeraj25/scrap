# module to fetch the url
import urllib3
# module to query the page
from bs4 import BeautifulSoup
# cssutils
import cssutils


# url to be scraped
shoe_url = "https://www.flipkart.com/mens-footwear/sports-shoes/pr?sid=osp%2Ccil%2C1cu&p%5B%5D=facets.brand%255B%255D%3DPuma&otracker=categorytree&page="
flipkart = 'https://www.flipkart.com'
# query the url and return the object in the variable page
http = urllib3.PoolManager()

"""
40 urls in total, looping on each url to create soup object every url
"""

# initialize lists for data frame
shoe_name = []
pic_url_0 = []
pic_url_1 = []
pic_url_2 = []
pic_url_3 = []
pic_url_4 = []
pic_url_5 = []
pic_url_6 = []
pic_url_7 = []
pic_url_8 = []

# function: append url in the list


def append_list(list_name, elem_url):
    image_url = ''
    if elem_url:
        # from image element extract url using cssutils
        style = cssutils.parseStyle(elem_url.get('style'))
        image_url = style['background-image']
        # cleaning the url IMPORTANT: This is getting url with 128 by 128 change it to 400 by 400
        image_url = image_url.replace('url(', '').replace(')', '')

        # append in corresponding list
        if list_name == 0:
            pic_url_0.append(image_url)
        if list_name == 1:
            pic_url_1.append(image_url)
        if list_name == 2:
            pic_url_2.append(image_url)
        if list_name == 3:
            pic_url_3.append(image_url)
        if list_name == 4:
            pic_url_4.append(image_url)
        if list_name == 5:
            pic_url_5.append(image_url)
        if list_name == 6:
            pic_url_6.append(image_url)
        if list_name == 7:
            pic_url_7.append(image_url)
        if list_name == 8:
            pic_url_8.append(image_url)
        if list_name == 9:
            pic_url_9.append(image_url)


# loop for pagination and iterate every page in the pagination,
for i in range(1, 2):  # todo-1: change the loop to 40
    shoe_page_url = shoe_url + str(i)
    # print(shoe_page_url)

    # Get the dome for soup from url
    shoe_list_response = http.request('GET', shoe_page_url)

    # create soup object from the fetched dome
    soup = BeautifulSoup(shoe_list_response.data, 'html.parser')

    # get shoe names
    names = soup.find_all('a', class_='_2cLu-l')
    # print(len(names))

    # loop for every page and iterate on every page from the single pagination page
    for name in names:
        shoe_name.append(name.get('title'))

        # get url for particular shoe store
        shoe_spec_url = flipkart+name.get('href')

        # get the dome object for shoe store
        shoe_store_response = http.request('GET', shoe_spec_url)

        # create soup  object for shoe store
        shoe_store_soup = BeautifulSoup(
            shoe_store_response.data, 'html.parser')

        # from shoe store get all images from the link
        shoe_store_images = shoe_store_soup.find_all('div', class_='_2_AcLJ')

        # storing different urls in lists
        for i in range(0, 10):
            if i in range(0, len(shoe_store_images)):
                append_list(i, shoe_store_images[i])
            else:
                append_list(i, None)
        # break outer loop
        break
