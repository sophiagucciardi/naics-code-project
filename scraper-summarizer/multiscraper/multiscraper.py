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
    
    paragraphs = raw_soup.find_all('p')

    return " ".join([p.get_text(" ", strip=True) for p in paragraphs])

#make file name from url
def file_name_from_url(url):
    file_name = url.split("/")[2].replace(".", "").replace('www', '')

    return f"{file_name}_soup.txt"

#list of sites to scrape---------------------------------------------------------------------------------------------------------------------
start_urls_list = ["https://bsmlawfirm.com/practice-areas","https://www.pinnacletravelstaffing.com/about","https://www.holisticaindiana.com/",
"https://www.lefrancoisfloralandgifts.com/about_us.php","https://k9coaturesalon.com/services/","https://enlightenvue.com/",
"https://gravyty.com/", "https://gravyty.com/alumni-engagement/", "https://gravyty.com/fundraising/","https://www.luxurgerynyc.com/services/",
"https://feldmaraesthetics.com/","https://www.smartwich.com/", "https://www.smartwich.com/smartwiches","https://www.moheganlakevet.com/", 
"https://www.moheganlakevet.com/services/wellness-services", "https://www.moheganlakevet.com/services/puppies-and-kittens", 
"https://www.moheganlakevet.com/services/diagnostic-services", "https://www.moheganlakevet.com/services/spay-neuter-and-surgical-services", 
"https://www.moheganlakevet.com/services/spay-neuter-and-surgical-services", "https://www.moheganlakevet.com/services/online-pharmacy",
"https://k-recruiting.com/en-US/about-us","https://www.besler.com/","https://njrealestateschool.education/","https://sollers.college/",
"https://www.beckyrickenbaker.net/","https://pureconfections.site/index.html","https://www.wiserhomeremodeling.com/",
"https://www.brightway.com/"," https://www.brightway.com/insurance/property", "https://www.brightway.com/insurance/vehicle", 
"https://www.brightway.com/insurance/other","https://dovetail.com/#recruit","https://www.payprop.com/us/features", 
"https://www.payprop.com/us", "https://www.assortedinternet.com/seoservices.php", "https://www.assortedinternet.com/hosting.php", 
"https://www.assortedinternet.com/cgiscripts.php", "https://www.assortedinternet.com/reseller.php","https://drzaydon.com/procedures/",
"https://www.simonschindler.com/practice-areas/","https://www.tinyteethsmiles.com/services/","https://www.southernheritagehome.com/",
"https://secur-tek.com/commercial-services/", "https://secur-tek.com/residential-services/","https://www.kinis.com/products",
"https://www.corlinproductions.com/services.html", "https://www.corlinproductions.com/about.html",
"https://sites.google.com/ualr.edu/ar-aims-science-preview-2021/about-ar-aims?authuser=0","https://retireto.com/what-we-do/", 
"https://retireto.com/investment-planning/", "https://retireto.com/retirement-income-spending-plan/", "https://retireto.com/estate-legacy-plan/",
"https://www.metisgp.com/","https://henryadams.com/services","https://www.bluebutterflycreations.net/","https://clermontdental.care/services/",
"https://www.brandywinevalleypsychiatry.com/#Services", "https://www.viper-drones.com/","https://www.lithoprintingjoplin.com/",
"https://www.cardinalgymnastics.com/","https://nouveaumedspa.com/#","https://www.gyaninfosystems.com/overview", "https://www.gyaninfosystems.com/services",
"https://anasaziwines.com/about-anasazi-wines/","https://www.studiodado.com/about-us/","https://www.avviato.com/","https://www.myspinc.com/",
"https://www.4urhires.com/#aboutus","https://www.thehrmanager.co/our-services","https://www.aconlv.org/","https://www.g4bygolpa.com/",
"https://mss.styleseat.com/aboutus/",
"https://signups.ws/products-and-services", "https://signups.ws/all-about-signups",
"https://www.esasolutions.com/services","https://www.relicx.ai/products/test-creation", "https://www.relicx.ai/products/test-execution", 
"https://www.relicx.ai/products/test-case-generation", "https://www.relicx.ai/","http://www.copackaz.com/","https://www.serialgrillersaz.com/about",
"https://www.bradshawfamilydental.com/p/dentist-Prescott-Valley-Dental+Services-p15027.asp", 
"https://www.bradshawfamilydental.com/p/sleep-apnea-Prescott-Valley-Sleep+Medicine-p14268.asp",
"https://www.arnitsolutions.com/","https://www.score.org/find-mentor/how-it-works","https://www.lakewoodflorist.org/about-us",
"https://courtyardsalonstexas.com/services-offered/","https://www.klassygreekemblems.com/","https://thekitchenstudios.net/","https://wildwestguitars.com/about",
"https://fortispay.com/solutions/","https://www.crdn.com/who-we-serve", "https://www.crdn.com/about-us","https://www.missionrebirth.com/",
"https://www.andellbrownlaw.com/","https://www.educaninebayarea.com/board-train","https://www.ftft.com/en/business.html", 
"https://www.ftft.com/en/about/who_we_are/","https://www.zonazerostudios.com/","https://www.northgabankruptcy.com/",
"https://www.currance.com/approach/","https://www.foothillspediatricdentist.com/","https://www.truesec.com/service",
"https://www.kssnyc.co/microsoft-365/", "https://www.kssnyc.co/systems-engineering/", "https://www.kssnyc.co/it-staffing/", 
"https://www.kssnyc.co/software-hardware-sales/", "https://www.kssnyc.co/cybersecurity/",
"https://virocell.com/what-we-do","https://elements.cloud/salesforce-change-intelligence-platform/?utm_campaign=Change%20Intelligence%20Q1%20FY23&utm_source=login-page",
"https://ohtsukaamerica.com/#company","https://www.wildwood.com/wildwood-101-introduction","https://www.wildwood.com/welcome-to-wildwood",
"https://www.fishdog.net/","https://www.redemptionfitnessholt.com/mission", "https://www.redemptionfitnessholt.com/",
"https://www.mizpahchicago.com/","https://www.thenestfurnishings.com/","https://austinstrategy.com/services", "https://austinstrategy.com/",
"https://www.rjeffrey.com/", "https://rjeffrey.com/industries_wotc/","https://www.theleague.global/services"
]

#-----------------------------------------------------------------------------------------------------------------------------------------------
#list for error urls
errored_urls = []

#for loop to scrape each site
for link in start_urls_list[:5]:
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

