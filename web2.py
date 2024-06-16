import os
import requests
from bs4 import BeautifulSoup
from proxycrawl.proxycrawl_api import ProxyCrawlAPI

# Define Google Image search URL
Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# Folder to save downloaded images
Image_Folder = 'Google_Images'

def main():
    # Create directory if it doesn't exist
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    
    # Start downloading images
    download_images()

def download_images():
    data = input('Enter your search keyword: ')
    num_images = int(input('Enter the number of images you want: '))
    
    print('Searching Images....')
    
    # Construct search URL
    search_url = Google_Image + '&q=' + data  # Add query parameter to Google_Image URL
    
    # Initialize ProxyCrawlAPI with your token
    api = ProxyCrawlAPI({'token': 'DPqfQJKC5BHVFGwo8AxQuA'})
    
    # Make request using ProxyCrawl API
    response = api.get(search_url, {'scroll': 'true', 'scroll_interval': '60', 'ajax_wait': 'true'})
    
    if response['status_code'] == 200:
        # Parse response using BeautifulSoup
        b_soup = BeautifulSoup(response['body'], 'html.parser')
        # Check if we have the right content
        print(f"Response length: {len(response['body'])}")
        
        # Update the selector to be more generic if the specific class doesn't work
        results = b_soup.findAll('img')
        
        count = 0
        imagelinks = []
        for res in results:
            try:
                link = res.get('data-src') or res.get('src') or res.get('data-iurl')
                if link and link.startswith('http'):
                    imagelinks.append(link)
                    count += 1
                    if count >= num_images:
                        break
            except KeyError:
                continue
        
        print(f'Found {len(imagelinks)} images')
        print('Start downloading...')
        
        for i, imagelink in enumerate(imagelinks):
            try:
                response = requests.get(imagelink)
                response.raise_for_status()
                imagename = os.path.join(Image_Folder, f'{data}{i+1}.jpg')
                
                with open(imagename, 'wb') as file:
                    file.write(response.content)
                
                print(f'Downloaded {imagename}')
            except requests.exceptions.RequestException as e:
                print(f'Failed to download image {i+1}: {e}')
    
        print('Download Completed!')
    else:
        print('Failed to retrieve search results')

if __name__ == '__main__':
    main()
