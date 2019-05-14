#import needed libraries
import time
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import spacy

def pickle_file(obj, filename):
    outfile = open(filename,'wb')
    pickle.dump(obj,outfile)
    outfile.close()
    return 'Pickled object!'
    
def open_pickle(file_location):
    pickle_in = open(file_location,"rb")
    pickeled = pickle.load(pickle_in)
    return pickeled

def comp_info_and_users(url):
    user_links = []
    page_options = []
    time.sleep(1)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    
    #find title--multiple h1 given for pages, so join them 
    title = soup.find('div',{'class':'biz-page-header'}).findAll('h1')
    company_source_name = ' '.join([x.text.strip() for x in title]).strip()

    #find all the links if multiple pages are given
    match = soup.findAll('div', {'class':'page-option'})# find all pages listed
    page_options.extend([x.a['href'] for x in match[1:]])
    time.sleep(1)
    
    #get users who've left comments on the first page
    user_match = soup.findAll('ul',{'class':'user-passport-info'})
    user_links.extend(['https://www.yelp.com'+x.a['href'] for x in user_match])
    
    #loop through review pages and get all users
    if len(page_options) >= 1:
        for url in page_options:
            time.sleep(1)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'lxml')

            user_match = soup.findAll('ul',{'class':'user-passport-info'})
            user_links.extend(['https://www.yelp.com'+x.a['href'] for x in user_match])
        
    return company_source_name,user_links

def request_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup

def get_reviews(i,soup,r_dict,company_source_name):
    review_headers = soup.findAll('a',{'class':'biz-name js-analytics-click'})
    r_dict['rev_comp_url'].extend(['https://www.yelp.com'+x['href'] for x in review_headers])
    r_dict['rev_company_name'].extend([x.text for x in review_headers])

    reviews_divs = soup.findAll('div',{'review'})
    one,two,three = ('<address>\n','\n    </address>','<br/>')
    r_dict['company_loc'].extend([' '.join(str(x.find('address')).replace(one,'')
                              .replace(two,'').strip().split(three)) for x in reviews_divs])
    r_dict['rev_comp_rating'].extend([float(x.find('div',{'class':'rating-large'})['title'][:3]) 
                                       for x in reviews_divs])
    
    reviews_4_comp = [x.p.text for x in reviews_divs]
    r_dict['rev_comp_reviews'].extend(reviews_4_comp)
    r_dict['userUrl'].extend([i]*len(reviews_4_comp))
    r_dict['company_source'].extend([company_source_name]*len(reviews_4_comp))
    
def reviews_top_pages_test(url,r_dict,review_num,driver):
    company_source_name,user_links = comp_info_and_users(url)
    
    if len(user_links) < 2:
        return 

    counter = 1
    
    for i in user_links:
        time.sleep(1)
        if counter > review_num:
            break
        if i not in r_dict['userUrl']:
            time.sleep(1)
            driver.get(i)
            time.sleep(0.5)
            try:
                city = driver.find_element_by_class_name('user-location').text
                if city in ('Queens, NY','Manhattan, NY','New York, NY','Brooklyn, NY','Manhattan, New York, NY'):
                    time.sleep(1)
                    driver.find_element_by_link_text('Reviews').click()
                    time.sleep(0.5)
                    driver.find_element_by_link_text('All Categories').click()
                    time.sleep(1)
                    driver.find_element_by_partial_link_text('Fitness & Instruction').click()
                    time.sleep(1)
                    reviews = driver.find_elements_by_class_name('review')
                    if len(reviews)>1:
                        comp_num_curr = len(set(r_dict['company_source']))
                        print(f'just did reviewer {counter} for company {comp_num_curr}')
                        counter += 1
                        time.sleep(1)
                        currentURL = driver.current_url
                        soup = request_page(currentURL)
                        #userName = soup.find('div',{'class':'user-profile_info arrange_unit'}).h1.text
                        page_options = soup.findAll('div',{'class':'page-option'})
                        pages = [x.a['href'] for x in page_options[1:]]
                        time.sleep(1)
                        get_reviews(i,soup,r_dict,company_source_name)

                        for url in pages:
                            soup = request_page(url)
                            get_reviews(i,soup,r_dict,company_source_name)
                    else:
                        time.sleep(1)

                else:
                    time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
        else:
            time.sleep(1)
            continue
            
    comp_num_curr = len(set(r_dict['company_source']))         
    return f'done with {comp_num_curr}'


def get_all_reviews(url_1,r_dict,review_num,company_count,starter_index):
    
    driver = webdriver.Chrome('/Users/elenasm7/.wdm/chromedriver/2.46/mac64/chromedriver') 
    reviews_top_pages_test(url_1,r_dict,review_num,driver)
    
    ok_locs = ['Brooklyn,NY', 'York,NY', 'Queens,NY','Bushwick,NY','Manhattan,NY','Astoria,NY ']
    
    for i in zip(r_dict['rev_company_name'][starter_index:],r_dict['rev_comp_url'][starter_index:],r_dict['company_loc'][starter_index:]):
        comp_num_curr = len(set(r_dict['company_source']))
        if comp_num_curr > company_count:
            break
        if (i[0] not in r_dict['company_source']) and ('CLOSED' not in i[0]) \
        and ((''.join(i[2].split(' ')[-3:-1])) in ok_locs) and ('MOVED' not in i[0]):
            if comp_num_curr % 100 == 0:
                filename = f'reviews_{comp_num_curr}'
                outfile = open(filename,'wb')
                pickle.dump(review_dict,outfile)
                outfile.close()
                time.sleep(1)
                for col in list(r_dict.keys()):
                    print(len(r_dict[col]))
                reviews_top_pages_test(i[1],r_dict,review_num,driver)
            else:
                time.sleep(0.5)
                reviews_top_pages_test(i[1],r_dict,review_num,driver)
                        
    driver.close()
    return pd.DataFrame(r_dict)

def clean_text_column(row):
    import string
    '''
    takes in a cell from the dataframe and removes all of the symbols from 
    string.punctuation ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'), and then lower
    cases each line.
    '''
    return row.translate(str.maketrans('', '', string.punctuation)).lower()


def return_lemma(review,nlp):
    doc = nlp(review)
    return ' '.join([word.lemma_ for word in doc])

def in_nyc(x):
    if 'NY' in x:
        return 1
    else: 
        return 0 

def replace_fixed_words(rev,df):
    words = rev.split(' ')
    cor_rev = []
    for word in words: 
        if word in list(df.words):
            cor_rev.append(df[df['words'] == word]['corrected'].item())
        else:
            cor_rev.append(word)
    return ' '.join(cor_rev)

def is_sample(url):
    tot_urls = list(set(new_user_selection['userUrl']))
    if url in tot_urls:
        return 1 
    else:
        return 0
    
def get_cats_and_review(ids):
    counter = 0
    headers = {
        'Authorization': 'Bearer {}'.format(api_key),
    }
    for i in ids:
        time.sleep(0.5)
        url = 'https://api.yelp.com/v3/businesses/'+i
        response = requests.get(url, headers=headers, params=url_params)
        comp_cats['review_count'].append(response.json().get('review_count'))
        comp_cats['rating'].append(response.json().get('rating'))
        comp_cats['ids'].append(i)
        try:
            comp_cats['categories'].append([i['alias'] for i in response.json().get('categories')])
        except:
            comp_cats['categories'].append(response.json().get('categories'))
        counter += 1
        print(f'just did {counter}')

def cat_join(cats):
    try: 
        return ' '.join(cats)
    except:
        return 0

