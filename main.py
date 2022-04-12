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
print(user, passwd)

if not user or not passwd:
    print("No user or password found")
    exit(1)

oc = owncloud.Client("https://cloud.marcotommoro.duckdns.org/")
oc.login(user, passwd)


for comune in comuni.comuni:
    query = f'comune "{comune}" "azzardo" ordinanza filetype:pdf | filetype:doc | filetype:docx | filetype:rtf'
    try:
        oc.mkdir(f"documenti/{comune}")
    except:
        pass

    for url in search(query, tld="co.in", num=10, stop=10, pause=2):
        print(url)
        try:
            name = url.split("/")[-1]
            if (
                not "pdf" in name
                and not "doc" in name
                and not "docx" in name
                and not "rtf" in name
            ):
                name += ".pdf"

            request.urlretrieve(url, f"docs/{name}")
            oc.put_file(f"documenti/{comune}/{name}", f"docs/{name}")
            os.remove(f"docs/{name}")
        except:
            pass
