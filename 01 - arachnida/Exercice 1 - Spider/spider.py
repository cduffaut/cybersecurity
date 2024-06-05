import argparse
import sys
import re
import os
import requests # python3 -m pip install requests
from bs4 import BeautifulSoup # python3 -m pip install beautifulsoup4
from urllib.parse import urljoin # to convert relative path in absolute URL
from urllib.parse import urlparse, urlunparse

# ------------------------------ parsing part ------------------------------

def custom_error_handler(message):
    if 'the following arguments are required: args' in message:
        print("Please enter the URL to scrap from, with the options [-rlp] URL.")
    else:
        print(message)
    sys.exit(1)

def valid_level(value):
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-l' and i + 2 == len(sys.argv):
            if is_url(sys.argv[i + 1]):
                return 5
        i += 1
    try:
        ivalue = int(value)
        if ivalue < 0:
            raise argparse.ArgumentTypeError("The depth level of the recursive download must be a positive integer.")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer.")
        
def validation_path(path):
    if re.match(r'https?://|www\.', path):
        return './data/'
    
    if os.path.exists(path) or path == './data/':
        return path
    else:
        print(f"Error: The provided path '{path}' is not a valid path.")
        sys.exit(1)

def is_url(url):
    try:
        # Clean and reformat the URL to ensure validity
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = 'http://' + url  # Assume HTTP if no scheme provided
        with requests.Session() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = session.get(url, headers=headers, timeout=5)
            return response.ok
    except requests.Timeout:
        print(f"Timeout occurred for URL: {url}")
        sys.exit(1)
    except requests.RequestException as e:
        return False

def is_valid_url(arg):
    if arg.startswith(("'", '"')) and arg.endswith(("'", '"')):
    arg = arg[1:-1]
    parsed = urlparse(arg)
    return bool(parsed.scheme and parsed.netloc)

for i, arg in enumerate(sys.argv):
    if arg == '-r' and i + 1 < len(sys.argv):
        next_arg = sys.argv[i + 1]
        if next_arg not in ['-l', '-p'] and not is_valid_url(next_arg):
            print(f"Error: Invalid argument '{next_arg}' after '-r'. Expected '-l', '-p', or a valid URL.")
            sys.exit(1)

parser = argparse.ArgumentParser(description="This script takes an URL as argument, and downloads all files attached to it.")

parser.error = custom_error_handler

parser.add_argument('-r', action='store_true', help='Enable recursive download')
parser.add_argument('-l', type=valid_level, nargs='?', const=5, default=float('inf'), help='Set the recursion depth (optional, default: infinite, 5 if -l is specified without a value)')
parser.add_argument('-p', type=validation_path, nargs='?', const='./data/', default='./data/', help='Set the download path (default: "./data/" if -p is specified without a value)')
parser.add_argument('url', nargs='?', help='The URL to scrape')

try:
    args = parser.parse_args()
except ValueError as e:
    print(f"Erreur : {e}")
    sys.exit(1)
except requests.ConnectionError as e:
    print("Erreur de connexion : Impossible de résoudre l'URL.")
    sys.exit(1)

if len(sys.argv) > 7:
    print("Too many arguments, please respect this format: [-rlp] URL.")
    sys.exit(1)

if len(sys.argv) == 1:
    print("Please enter arguments under the format: [-rlp] URL.")
    sys.exit(1)

i = 1

arg  = sys.argv[i]
if arg == '-r':
    if (sys.argv[i + 1] != '-l' and sys.argv[i + 1] != '-p') and not is_url(sys.argv[i + 1]):
        print("Error: There are elements that do not fit the format: [-rlp] URL.")
        sys.exit(1)

r = 0
l = 0
p = 0

i = 1

while i < len(sys.argv):
    arg  = sys.argv[i]
    if arg == '-r':
        r += 1
    elif arg == '-l':
        l += 1
    elif arg == '-p':
        p += 1
    i += 1

if r > 1 or l > 1 or p > 1:
    print("Error: There is two times, or more, the same option... : [-rlp].")
    sys.exit(1)

i = 1

while i < len(sys.argv):
    arg  = sys.argv[i]
    if arg != '-r' and arg != '-l' and arg != '-p':
        if i != len(sys.argv) - 1 and sys.argv[i - 1] != '-r' and sys.argv[i - 1] != '-l' and sys.argv[i - 1] != '-p':
            print("Error: There is elements that does not fit the format: [-rlp] URL.")
            sys.exit(1)   
    i += 1

i = 1
r = 0
l = 0
p = 0

# check if the options are in the right order
while i < len(sys.argv):
    arg  = sys.argv[i]
    if arg == '-r':
        r = i
    if arg == '-l':
        l = i
    if arg == '-p':
        p = i
    i += 1

if p != 0 and p < l:
    print("Error: Options are not in the right order : [-rlp].")
    sys.exit(1)

if p != 0 and p < r:
    print("Error: Options are not in the right order : [-rlp].")
    sys.exit(1)

if l != 0 and l < r:
    print("Error: Options are not in the right order : [-rlp].")
    sys.exit(1)

for i in range(1, len(sys.argv) - 1): # check if any other args is an URL or not
    if is_valid_url(sys.argv[i]):
        print(f"Error: '{sys.argv[i]}' should not be placed here.")
        sys.exit(1)

last_argument = sys.argv[-1].strip()  # Remove any leading/trailing whitespace
if last_argument.startswith(("'", '"')) and last_argument.endswith(("'", '"')):
    last_argument = last_argument[1:-1]

if not is_valid_url(last_argument):
    print(f"Erreur : The URL '{last_argument}' is not valid.\nFormat expected: [-rlp] URL.")
    sys.exit(1)

if is_url(last_argument) is None:
    sys.exit(1) 
else:
    print(f"\n✅ URL is valid: {last_argument}")

# ------------------------------ end of parsing ------------------------------

print ('\n-r value: ' + str(args.r))
print ('-l value: ' + str(args.l))
print ('-p value: ' + str(args.p) + '\n')

# ------ [ python scraper to get the images (recursive way) ] Aka "The Real Deal" ------

# found the images in the HTML pages
try:
    response = requests.get(last_argument)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    download_images = [
        img['src'] for img in images 
        if 'src' in img.attrs and re.search(r'\.(jpg|jpeg|png|gif|bmp)$', img['src'], re.I)
    ]
except requests.RequestException as e:
    print(f"Request error : {e}")
    sys.exit(1)

visited = set()  # Stock URLs already visited
queue = []       # URLs to visit 

# Download images if they're in the right format
def download_image(img_url, base_url):
    full_url = urljoin(base_url, img_url)
    if re.search(r'\.(jpg|jpeg|png|gif|bmp)$', full_url, re.IGNORECASE):
        response = requests.get(full_url)
        directory = args.p
        if directory == './data/':  # Check if it the default path
            os.makedirs(directory, exist_ok=True)  # Create the file if it does not exist
        image_path = os.path.join(directory, os.path.basename(full_url))
        with open(image_path, 'wb') as f:
            f.write(response.content)


def download_images_from_page(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to access {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')
            if img_url:
                download_image(urljoin(url, img_url), url)
                print(f"Success to access {url}")

    except requests.ConnectionError as e:
        print("Erreur de connexion : Impossible de résoudre l'URL.")
    except requests.Timeout as e:
        print("Erreur : La requête a dépassé le temps d'attente.")
    except requests.RequestException as e:
        print("Erreur lors de la requête : ", e)

def download_recursively(url, visited=set(), depth=0):
    if url in visited or depth > args.l:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        download_images_from_page(url) 
        
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and not href.startswith(('mailto:', 'javascript:')):  # Ignore mailto and javascript links that conduce to error
                full_url = urljoin(url, href)
                download_recursively(full_url, visited, depth + 1)
    except requests.Timeout:
        print(f"Timeout occurred for URL: {url}. Skipping to next link.")
        return 
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return

def main():
    try:
        if args.r:
            download_recursively(last_argument)
        else:
            download_images_from_page(last_argument)
    except KeyboardInterrupt:
        print("\n[Info] Script execution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()