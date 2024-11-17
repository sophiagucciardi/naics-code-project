#imports
from bs4 import BeautifulSoup
from selenium import webdriver
import re, time, os

#FUNCTIONS--------------------------

#define driver
driver = webdriver.Firefox()

#get soup for page
def soupify_url(url, driver=driver):
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')

#gets links for page
def get_links_in_soup(soup, origin_url):
    origin_domain = origin_url[7:].strip("/") # gets domain from full url

    valid_links = [link.get('href') for link in soup.find_all('a') if "/" in link.get('href')]
    full_urls = [link for link in valid_links if f"https://{origin_domain}" in link] # if websites use full urls to reference pages
    path_urls = [link.split("#")[0] for link in valid_links if re.search("^/", link)] # get paths in the website, and remove # marks at end
    
    path_urls = [f"https://{origin_domain}{path}" for path in path_urls] # add domain to path

    full_urls = full_urls
    full_urls.extend(path_urls)
    
    return list(set(full_urls)) # remove duplicates

#scraper
def scraper(link, driver=driver):
    print(f"Scraping {link}")

    driver.get(link)
    time.sleep(2)

    html = driver.page_source
    raw_soup = BeautifulSoup(html, features="html.parser")

    #remove white space
    return raw_soup.get_text(" ", strip=True)

#make file name from url
def file_name_from_url(url):
    file_name = url.split("/")[2].replace(".", "").replace('www', '')

    return f"{file_name}_soup.txt"

#list of sites to scrape---------------------------------------------------------------------------------------------------------------------
start_urls_list = ["https://www.bsmlawfirm.com/", "https://www.pinnacletravelstaffing.com/", "https://www.holisticaindiana.com/",
    "https://www.lefrancoisfloralandgifts.com/", "https://www.k9coaturesalon.com/", "https://www.enlightenvue.com/", "https://www.gravyty.com/",
    "https://www.luxurgerynyc.com/", "https://www.feldmaraesthetics.com/", "https://www.smartwich.com/", "https://www.moheganlakevet.com/",
    "https://www.k-recruiting.com/en-US/", "https://www.besler.com/", "https://www.njrealestateschool.education/","https://www.sollers.edu/",
    "https://www.beckyrickenbaker.net/", "https://www.thepureconfections.com/", "https://www.wiserhomeremodeling.com/",
    "https://www.quantuvos.com/", "https://www.brightway.com/", "https://www.dovetail.com/", "https://www.payprop.com/us",
    "https://www.assortedinternet.com/", "https://www.drzaydon.com/", "https://www.simonschindler.com/", "https://www.tinyteethsmiles.com/", 
    "https://www.southernheritagehome.com/", "https://www.secur-tek.com/", "https://www.kinis.com/", "https://www.corlinproductions.com/",
    "https://www.sites.google.com/ualr.edu/ar-aims-science-preview-2021/home", "https://www.retireto.com/", "https://www.metisgp.com/",
    "https://www.henryadams.com/", "https://www.bluebutterflycreations.net/", "https://www.clermontdental.care/",
    "https://www.brandywinevalleypsychiatry.com/", "https://www.viper-drones.com/", "https://www.lithoprintingjoplin.com/",
    "https://www.cardinalgymnastics.com/", "https://www.nouveaumedspa.com/", "https://www.gyaninfosystems.com/", "https://www.anasaziwines.com/",
    "https://www.studiodado.com/", "https://www.avviato.com/", "https://www.myspinc.com/", "https://www.4urhires.com/", "https://www.decisiongps.com",
    "https://www.thehrmanager.co/", "https://www.aconlv.org/", "https://www.g4bygolpa.com/", "https://mss.styleseat.com/aboutus/",
    "https://www.signups.ws/", "https://www.esasolutions.com/", "https://www.relicx.ai/",
    "https://store.ameliocenterprises.com/","https://www.serialgrillersaz.com/","https://www.bradshawfamilydental.com/",
    "https://www.arnitsolutions.com/", "https://www.score.org/", "https://www.lakewoodflorist.org/",
    "https://www.courtyardsalonstexas.com/", "https://www.klassygreekemblems.com/", "https://www.thekitchenstudios.net/",
    "https://www.wildwestguitars.com/", "https://www.paymentlogistics.com/", "https://www.crdn.com/", "https://www.missionrebirth.com/", 
    "https://www.andellbrownlaw.com/","https://www.educaninebayarea.com/", "https://www.ftft.com/", "https://www.zonazerostudios.com/", 
    "https://www.northgabankruptcy.com/","https://www.currance.com/", "https://www.foothillspediatricdentist.com/", "https://www.truesec.com/", 
    "https://www.kssnyc.co/", "https://www.virocell.com/","https://www.elements.cloud/", "https://www.ohtsukaamerica.com/", "https://www.wildwood.com/alosis-bistro", 
    "https://www.fishdog.net/","https://www.redemptionfitnessholt.com/", "https://www.mizpahchicago.com/", "https://www.thenestfurnishings.com/", 
    "https://www.austinstrategy.com/","https://www.rjeffrey.com/", "https://www.theleague.global/"
]

#-----------------------------------------------------------------------------------------------------------------------------------------------
#list for error urls
errored_urls = []

#for loop to scrape each site
for link in start_urls_list:
    if not os.path.exists(f"scraped/{file_name_from_url(link)}"):
        soups = []
        #get all links accessible from homepage
        try:
            link_soup = soupify_url(link)
            links = get_links_in_soup(link_soup, link)
            links
        
            for link in links:
                processed_soup = scraper(link)
                soups.append(str(processed_soup))
                
            #add scraped content to unique text file for each site
            if not os.path.exists("scraped"):
                os.makedirs("scraped")

            with open(f"scraped/{file_name_from_url(link)}", "a") as file:
                for line in soups:
                    file.write(line)
                    file.write("\n")

        except Exception as e: 
            errored_urls.append(link)
            print("\n\nError: ", link, "could not be scraped because:")
            print(e, "\n\n")
            continue

driver.close()

#show all error urls
print("Errored urls:")
for url in errored_urls:
    print(url)

