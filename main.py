import os

try:
    from urllib import request

    import owncloud
    from googlesearch import search

    import comuni

except ImportError:
    print("No module  found")

user = os.environ.get("OC_USER")
passwd = os.environ.get("OC_PASSWORD")

if not user or not passwd:
    print("No user or password found")
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

for comune in comuni.comuni:
    codice_nome = f'{comune["codice"]}_{comune["nome"]}'
    query = f'comune "{comune["nome"]}" "azzardo" ordinanza filetype:pdf | filetype:doc | filetype:docx | filetype:rtf'

    try:
        oc.mkdir(f"documenti/{codice_nome}")
    except owncloud.ResponseError as e:
        print(e)
        pass

    print(query)

    for url in search(query, num=10, pause=2):
        print(url)
        if url in url_list:
            continue

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
