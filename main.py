import json
import os

import requests as req
from dotenv import load_dotenv

load_dotenv()

try:
    from urllib import request

    import owncloud
    from googlesearch import search

    import comuni

except ImportError:
    print("No module  found")

user = os.environ.get("OC_USER")
passwd = os.environ.get("OC_PASSWORD")
api_key = os.environ.get("API_KEY")

if not user or not passwd or not api_key:
    print("No user or password or api_key found")
    exit(1)

oc = owncloud.Client("https://cloud.marcotommoro.duckdns.org/")
oc.login(user, passwd)

url_list = []

if os.path.exists("./urls.txt"):
    with open("./urls.txt", "r") as fr:
        url_list = fr.readlines()
        fr.close()

if not os.path.exists("./docs") or not os.path.isdir("./docs"):
    os.mkdir("./docs")


# set up the request parameters
params = {
    "api_key": api_key,
    "q": "",
    "location": "Italy",
    "gl": "it",
    "hl": "it",
    "google_domain": "google.it",
    "num": "10",
}


for comune in comuni.comuni:
    codice_nome = f'{comune["codice"]}_{comune["nome"]}'
    query = f'comune "{comune["nome"]}" "azzardo" ordinanza filetype:pdf | filetype:doc | filetype:docx | filetype:rtf'

    print(codice_nome)
    try:
        oc.mkdir(f"documenti/{codice_nome}")
    except owncloud.ResponseError as e:
        print(e)
        pass

    params["q"] = query

    api_result = req.get("https://api.valueserp.com/search", params)
    print("remaining: ", api_result.json()["request_info"]["topup_credits_remaining"])

    for result in api_result.json()["organic_results"]:
        url = result["link"]

        if url in url_list:
            print(url, "already downloaded.")
            continue

        print("fetching...", url)
        url_list.append(url)

        try:
            name = url.split("/")[-1]
            if (
                not ".pdf" in name
                and not ".doc" in name
                and not ".docx" in name
                and not ".rtf" in name
            ):
                name += ".pdf"

            request.urlretrieve(url, f"docs/{name}")
            oc.put_file(f"documenti/{codice_nome}/{name}", f"docs/{name}")
            os.remove(f"docs/{name}")

            with open("./urls.txt", "a") as fw:
                fw.write(url + "\n")
                fw.close()

        except Exception as e:
            print(e)
            pass
