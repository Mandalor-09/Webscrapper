import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import base64

def scrape_product_data(search_query):
    base_url = "https://www.flipkart.com/"
    search_url = base_url + f"search?q={search_query}"

    all_data = []

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        html_page = response.content

        beautify_html_page = BeautifulSoup(html_page, 'lxml')

        total_links = []
        for container in beautify_html_page.find_all("div", {'class': '_2kHMtA'}):
            product_link = base_url[:-1] + container.a["href"]
            total_links.append(product_link)

        for link in total_links:
            product_page_response = requests.get(link)
            product_page_response.raise_for_status()
            product_page = BeautifulSoup(product_page_response.content, 'lxml')

            product_name_element = product_page.find('h1', {'class': 'yhB1nd'})
            product_name = product_name_element.span.text
            
            product_images = product_page.find_all('img', {'class': 'q6DClP'})
            image_data_list = []


            for i,img in enumerate(product_images):
                src = img['src']
                image_data = requests.get(src).content
                # Extract the image filename from the URL
                image_filename = f'static/{product_name}_{i}.jpeg'
    
                # Save the image content to a file in the 'static' folder
                with open(image_filename, 'wb') as f:
                    f.write(image_data)
                    print(f"Image '{image_filename}' downloaded successfully.")
                
                # Add image information to the list
                image_info = {
                    'filename': image_filename,
                }
                image_data_list.append(image_info)


            product_star_rating_element = product_page.find('div', {'class': '_3LWZlK'})
            product_star_rating = float(product_star_rating_element.text) if product_star_rating_element else None

            product_price = int(product_page.find_all('div', {'class': '_16Jk6d'})[0].text.replace(',', '').replace('₹',''))

            total_rating_element = product_page.find('span', {'class': '_2_R_DZ'})
            if total_rating_element and total_rating_element.span:
                total_rating_text = total_rating_element.span.text
                total_rating_parts = total_rating_text.split()
                
                if len(total_rating_parts) >= 2:
                    product_rating = int(total_rating_parts[0].replace(',', ''))
                    product_review_count = int(total_rating_parts[-2].replace(',', ''))
                else:
                    product_rating = None
                    product_review_count = None
            else:
                product_rating = None
                product_review_count = None

            feature_elements = product_page.find_all('div', {'class': '_2418kt'})[0].find_all('li', {'class': '_21Ahn-'})
            product_features = [li.text for li in feature_elements]

            feedback = {}
            for feedback_container in product_page.find_all('div', {'class': '_2wzgFH'}):
                person_element = feedback_container.find_all('div', {'class': '_3n8db9'})[0]
                person = person_element.div.p.text
                comment = feedback_container.div.p.text
                feedback[person] = comment

            product_data = {
                'name': product_name,
                'images': image_data_list,
                'features': product_features,
                'star_rating': product_star_rating,
                'price': product_price,
                'rating': product_rating,
                'review_count': product_review_count,
                'feedback': feedback
            }

            all_data.append(product_data)

    except requests.exceptions.RequestException as e:
        print("Error:", e)
    reviews = all_data
    return reviews

