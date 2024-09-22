
import requests
from pathlib import Path

response = requests.api.request('GET', 'https://string-db.org/api/json/version')

version = response.json()[0]['string_version']

print(version)

links_table = f'https://stringdb-downloads.org/download/protein.links.v{version}.txt.gz'
species_table = f'https://stringdb-downloads.org/download/species.v{version}.txt'
proteins_table = f'https://stringdb-downloads.org/download/protein.info.v{version}.txt.gz'
proteins_aliases_table = f'https://stringdb-downloads.org/download/protein.aliases.v{version}.txt.gz'

tables = [links_table, species_table, proteins_table, proteins_aliases_table]

def download_file(url):

    local_filename = url.split('/')[-1]

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(Path('DB', local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename


# download_file(species_table)

for table in tables:
    download_file(table)


