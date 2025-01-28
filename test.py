import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Print or return the full HTML content
        return soup.prettify()
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Enter the URL of the website you want to scrape
    website_url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/detail/4770/#tab_registration"  # Replace with your desired website
    html_content = scrape_website(website_url)
    
    # Save the content to a file for analysis or print it
    with open("website_data.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("Website data saved to 'website_data.html'")
