def main(path, filename):
    os.makedirs(path, exist_ok=True)
    url = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
    wget.download(url, path+'/'+filename)