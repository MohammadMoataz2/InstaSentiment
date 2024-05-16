import requests
from bs4 import BeautifulSoup
import pandas as pd

import re


def open_souq_scraping(url_of_posts,number_of_pages):
    url_of_posts = url_of_posts[:-1]

    open_sooq_url = "https://jo.opensooq.com"

    dict_for_items = {}

    df_items = pd.DataFrame()



    # Loop through multiple pages
    for page_number in range(1, number_of_pages + 1):  # Adjust the range accordingly

        try:

        
            web_path = url_of_posts + str(page_number)

            response = requests.get(web_path)
            soup = BeautifulSoup(response.text, 'html.parser')

            listing_post = soup.find("section", {"id": "serpMainContent"}).find_all("div", class_="sc-21acf5d5-0 fxpjMg mb-32 relative radius-8 grayHoverBg whiteBg boxShadow2")


            listing_post_urls = [post.find("a")["href"] for post in listing_post][:15]



            try: 

                for url in listing_post_urls:

                    try:

                        url_item = url
                        
                        response_item = requests.get(url_item)
                        soup_item = BeautifulSoup(response_item.text, 'html.parser')

                        car_info_table = soup_item.find("section", id="PostViewInformation")
                        row_info = car_info_table.find_all("li" , class_ = "postCpsSearchSource flex flexSpaceBetween alignItems radius-8 width-49")

                        dict_only_one_item = {two_section.find("p").text: str(two_section.find("a").text).replace(",",";") for two_section in row_info}

                        # Extracting price
                        price_element = soup_item.find("section", id="postViewCardDesktop").find("div", class_="flex alignItems relative priceColor bold font-30 width-fit")
                        dict_only_one_item["price"] = str(price_element.text).replace(",",";") if price_element else "N/A"


                        location_element = soup_item.find("section", id="postViewLocation").find("a")
                        dict_only_one_item["location"] = str(location_element.text).replace(",",";") if location_element else "N/A"


                        desc_element = soup_item.find("section", id="postViewDescription").find_all("p")
                        dict_only_one_item["Description"] = " ".join([desc_element[p_ele].text for p_ele in range(len(desc_element))]).replace(",",";")



                        dict_only_one_item["url"] = str(url_item).replace(",",";")

                        dict_only_one_item["page_num"] = page_number





                        pattern = r'/(\d+)/'
                        # Use re.search to find the match
                        match = re.search(pattern, url_item)
                        # Extract the ID from the match
                        if match:
                            extracted_id = match.group(1)
                            dict_only_one_item["item_id"] = extracted_id   
                        else:
                            dict_only_one_item["item_id"] = "ID not found"



                        owner_element = soup_item.find("section", id="PostViewOwnerCard")

                        url_owner_element = owner_element.find("a").get('href')
                        dict_only_one_item["owner_url"] = str(open_sooq_url + url_owner_element).replace(",",";") if url_owner_element else "N/A"


                        name_owner_element = owner_element.find("a").find("h3").text
                        dict_only_one_item["owner_name"] =  str(name_owner_element).replace(",",";") if name_owner_element else "N/A"


                        since_owner_element = owner_element.find("a").find("span" , class_ = "ltr inline").text
                        dict_only_one_item["owner_mem_since"] =  str(since_owner_element).replace(",",";") if since_owner_element else "N/A"

                        dict_only_one_item["title"] = soup_item.find("h1").text






                        extra_info = soup_item.find("section", id="PostViewInformation").find_all("li", class_="postCpsSearchSource width-100 radius-8 flex flexSpaceBetween flexWrap mt-8")


                        for two_section in extra_info:
                                
                                all_p = two_section.find_all("p")

                            
                                dict_only_one_item[all_p[0].text] = str(all_p[1].text).replace(",",";")












                        dict_for_items[soup_item.find("h1").text] = dict_only_one_item

                        for i in dict_for_items.keys():
                            df_items = pd.concat([df_items,pd.DataFrame([dict_for_items[i].values()],columns = dict_for_items[i].keys())],axis = 0 , ignore_index=True)

                        df_items.drop_duplicates(inplace=True)
                        df_items.to_csv("apa_test.csv")




                        

                        
                    except Exception as e:

                        print(f"type of exception {type(e)} The Exception {e}")

                        print(f"there was error in {page_number} the : {open_sooq_url + url}")


                        continue

                # Concatenate the data from each page to the DataFrame

                print(f"Page number {page_number} finished")
                print(len(dict_for_items))
                print(len(df_items))



            except:

                print(f"there was error in {page_number} the : {open_sooq_url + url}")
                continue
        except Exception as e:

            
            print(f"type of exception {type(e)} The Exception {e}")

            continue


    return df_items,dict_for_items
            
        