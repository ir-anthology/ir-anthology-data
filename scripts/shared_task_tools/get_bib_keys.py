import requests
from bs4 import BeautifulSoup
import time
import re
import argparse

#returns html text
def get_text(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, "html.parser")

#returns bibkeys for found paper
def get_bibkey(url):
    text = get_text(url)
    bibtex = text.find("a", {"class": "btn btn-secondary btn-sm"}).get("href")
    bibkey = bibtex.split("/")[3].split(".")[0]
    return bibkey

#gets Results of Search in the IR-Anthology by papername and year(published)
def get_ir_results(papername, year):
    #to prevent ddos
    time.sleep(2)

    rst = papername

    unsafe_chars = "@"
    papernameForSearch = re.sub(" : ", ": ", papername)
    papernameForSearch = re.sub(" / ", "/ ", papernameForSearch)
    papernameForSearch = re.sub(" ", "+", papernameForSearch)
    papernameForSearch = re.sub(unsafe_chars, "+", papernameForSearch)

    link = "https://ir.chatnoir.eu/?q=" + papernameForSearch

    try:
        text = get_text(link)
        results = text.findAll("article")
        if len(results) >= 1:
            tmp = []
            for art in results:
                paperyear = art.find("div", {"class": "meta"}).findAll("a")[1]
                if paperyear == str(year):
                    tmp.append(art)
            if len(tmp) != 0:
                print("Search for " + papername + " wasn't unambiguous")
            else:
                link = text.find("article").find("h2").find("a").get("href")
                rst = get_bibkey(link)
        elif len(results) != 0:
            link = results[0].find("h2").find("a").get("href")
            rst = get_bibkey(link)
        else:
            print("No result found while searching for: " + papername)

    except ConnectionError:
        print("something went wrong while searching for: " + papername)
        print(ConnectionError)

    return rst

#returns all tasks and their papers from trec
def get_paper_from_trec(url):

    text = get_text(url)
    tasks = text.findAll("center")[2:]
    tasks = [task.find("b").text for task in tasks]

    papers_tmp = text.findAll("dl")[1:]
    papers_tmp = [task.findAll("li")for task in papers_tmp]
    papers = []
    for task in papers_tmp:
        papers.append([paper.find("b").text for paper in task])

    return tasks, papers

#returns all tasks and their papers from ceur
def get_paper_from_ceur(url):
    text = get_text(url)

    text = text.find("div", {"class":"CEURTOC"})
    h3 = text.findAll("h3")
    ul = text.findAll("ul")[1:]
    tasksnames = [task.text for task in h3]
    papers = []
    for tmp in ul:
        li = tmp.findAll("li")
        taskpapers = [text.find("span", {"class": "CEURTITLE"}).text for text in li]
        papers.append(taskpapers)

    return tasksnames, papers

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('origin', type=str, nargs='?', default="trec",#ceur
                        help='origin of the proceeding(currently trec or ceur)')

    parser.add_argument('proceeding_url', type=str, nargs='?', default="https://trec.nist.gov/pubs/trec29/xref.html",#http://ceur-ws.org/Vol-2696/
                        help='url to the proceeding')

    parser.add_argument('year', type=int, nargs='?', default=2020,
                        help='year of the proceeding')

    args = parser.parse_args()

    if args.origin == "trec":
        tasknames, taskpapers = get_paper_from_trec(args.proceeding_url)
    if args.origin == "ceur":
        tasknames, taskpapers = get_paper_from_ceur(args.proceeding_url)

    for task, name in zip(taskpapers, tasknames):
        print(name)
        keys = [get_ir_results(key, args.year) for key in task]
        print("Overviewpaper:")
        print(keys[0])
        print("Participantpaper:")
        print(keys[1:])
