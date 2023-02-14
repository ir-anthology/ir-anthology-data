import requests
from bs4 import BeautifulSoup
import time
import re
import argparse
import json
import Levenshtein as lev

def id(name):
    id = re.sub("[^A-Za-z]+", "", name)
    return id.lower()


# returns html text as beautifulSoup
def get_text(origin, online):
    if online:
        r = requests.get(origin)
        soup = BeautifulSoup(r.text, "html.parser")
    else:
        with open(origin,  encoding="utf8") as fp:
            soup = BeautifulSoup(fp, "html.parser")
    return soup


# returns bibkeys for found paper
def get_bibkey(url):
    text = get_text(url, True)
    bibtex = text.find("a", {"class": "btn btn-secondary btn-sm"}).get("href")
    bibkey = bibtex.split("/")[3].split(".")[0]
    return bibkey


# gets Results of Search in the IR-Anthology by papername and year(published)
def get_ir_results(papername, year, venue):
    # to prevent ddos
    time.sleep(2)

    rst = papername

    papername = papername.strip()
    papername = re.sub(" +", " ", papername)
    papername = re.sub("--", "-", papername)
    papername = re.sub("\n", " ", papername)

    unsafe_chars = "[@&]"
    papernameForSearch = re.sub(" : ", ": ", papername)
    papernameForSearch = re.sub(" / ", "/ ", papernameForSearch)
    papernameForSearch = re.sub(unsafe_chars, " ", papernameForSearch)

    url = "https://ir.chatnoir.eu/api/v1/_search"
    key =''
    try:
        with open("key.txt") as test:
            key = test.read()
    except:
        print("apikey not found, You can get one by contacting the webis group and saving under key.txt")
    search = {}
    search["apikey"] = key
    search["query"] = papernameForSearch
    search["pretty"] = True
    search["venue"] = venue
    #search["year"] = year
    try:
        ans = requests.post(url, json=search, timeout=15)
    except:
        papernameForSearch = papernameForSearch.rsplit(" ", 3)[0]
        search["query"] = papernameForSearch
        try:
            ans = requests.post(url, json=search, timeout=20)
        except:
            print("No result found while searching for: " + papername)
            return papername

    if ans.status_code == 200:
        results = json.loads(ans.text)["results"]
        results = [entry for entry in results if (int)(entry["year"]) == year]



        for entry in results:
            if re.sub("â€™", "-", BeautifulSoup(entry["title"], features="lxml").text) in papername:
                return get_bibkey(entry["cache_uri"])

        url = ""
        ratio = 0
        for entry in results:
            new_ratio = lev.ratio(BeautifulSoup(entry["title"], features="lxml").text, papername)
            if new_ratio >= ratio:
                ratio = new_ratio
                url = entry["cache_uri"]
        if ratio > 0.7:
            return get_bibkey(url)



    print("No fitting result found while searching for: " + papername)
    return papername

    # link = "https://ir.chatnoir.eu/?q=" + papernameForSearch
    #
    # try:
    #     text = get_text(link)
    #     results = text.findAll("article")
    #     if len(results) >= 1:
    #         tmp = []
    #         for art in results:
    #             paperyear = art.find("div", {"class": "meta"}).findAll("a")[1]
    #             if paperyear == str(year):
    #                 tmp.append(art)
    #         if len(tmp) != 0:
    #             print("Search for " + papername + " wasn't unambiguous")
    #         else:
    #             link = text.find("article").find("h2").find("a").get("href")
    #             rst = get_bibkey(link)
    #     elif len(results) != 0:
    #         link = results[0].find("h2").find("a").get("href")
    #         rst = get_bibkey(link)
    #     else:
    #         print("No result found while searching for: " + papername)
    #
    # except ConnectionError:
    #     print("something went wrong while searching for: " + papername)
    #     print(ConnectionError)
    #
    # return rst


# returns all tasks and their papers from trec
def get_paper_from_trec(url):
    text = get_text(url, args.online)
    #2001<
    tasks = text.findAll("center")
    #tasks = text.findAll("center")[2:]
    # tasks = text.findAll("center")[2:-1] only 2016
    tasks = [task.find("b").text for task in tasks]

    papers_tmp = text.findAll("dl")[1:]
    # only sometimes!!!
    papers_tmp = papers_tmp[::2]
    #>2009
    #papers_tmp = [task.findAll("li") for task in papers_tmp]
    #<2008
    #papers_tmp = [task.findAll("dt") for task in papers_tmp]
    #<2003
    papers_tmp = [task.findAll("dd") for task in papers_tmp]
    papers = []
    for task in papers_tmp:
        #papers.append([paper.find("b").text for paper in task])
        #papers.append([BeautifulSoup(paper.text, "lxml").get_text(strip=True) for paper in task])
        papers.append([BeautifulSoup(paper.text, "lxml").get_text(strip=True).rsplit(",", 1)[0] for paper in task if BeautifulSoup(paper.text, "lxml").get_text(strip=True) != ""])


        # tmp = [paper.text for paper in task]
        # tmp = [entry.split("\n\n") for entry in tmp]
        # papers1 = []
        # for i in tmp:
        #     for x in i[1:]:
        #         papers1.append(x)
        # papers.append(papers1)


    return tasks, papers


# returns all tasks and their papers from ceur
def get_paper_from_ceur(url):
    text = get_text(url, args.online)

    text = text.find("div", {"class": "CEURTOC"})
    #h3 = text.findAll("h3")[1:-1]
    h3 = text.findAll("h3")
    #ul = text.findAll("ul")[1:-1]
    ul = text.findAll("ul")
    tasksnames = [task.text for task in h3]
    papers = []
    for tmp in ul:
        li = tmp.findAll("li")
        taskpapers = [text.find("span", {"class": "CEURTITLE"}).text for text in li]
        papers.append(taskpapers)

    return tasksnames, papers


def get_paper_from_ceur_medival(url):
    text = get_text(url, args.online)

    text = text.find("div", {"class": "CEURTOC"})
    h3 = text.findAll("h3")
    ul = text.findAll("ul")
    tasksnames = [task.text for task in h3]
    papers = []
    taskpapers = []
    for tmp in ul:
        taskpapers.append(re.sub("\n", "", re.sub(" +", " ", tmp.find("span", {"class": "CEURTITLE"}).text.strip())))
        if tmp.next_sibling.next_sibling == None or tmp.next_sibling.next_sibling.name == "h3":
            papers.append(taskpapers)
            taskpapers = []
    return tasksnames, papers


def get_paper_from_ntcir(url):
    text = get_text(url, args.online)
    h2 = text.findAll("h2")
    tmp = h2[1].findAllNext()
    tasknames = []
    papers = []
    tmp2 = []
    for tag in tmp:
        if tag.name == "li":
            tmp2.append(tag.find("a").text)
        elif tag.name == "h3":
            tasknames.append(tag.text[1:-1])
            papers.append(tmp2)
            tmp2 = []
    papers.append(tmp2)
    papers = papers[1:]
    return tasknames, papers


def create_dict(tasknames, taskpapers, conf):
    dict = {}
    if conf == "FIRE" or conf == "CLEF" or conf == "TREC":
        dict["id"] = id(conf)
        dict["label"] = conf
        dict["tasks"] = []
        for task, name in zip(taskpapers, tasknames):
            print(task, name)
            dict2 = {}
            dict2["id"] = id(name)
            dict2["label"] = name
            dict2["overviewpapers"] = []
            dict2["participantpapers"] = []
            for paper in task:
                key = get_ir_results(paper, args.year, args.proceeding_name)
                if "Overview" in paper:
                    dict2["overviewpapers"].append(key)
                else:
                    dict2["participantpapers"].append(key)
            dict2["link"] = ""
            dict["tasks"].append(dict2)
    else:
        dict["id"] = id(conf)
        dict["label"] = conf
        dict["tasks"] = []
        for task, name in zip(taskpapers, tasknames):
            print(task, name)
            dict2 = {}
            dict2["id"] = id(name)
            dict2["label"] = name
            dict2["overviewpapers"] = []
            dict2["participantpapers"] = []
            i = 0
            for paper in task:
                key = get_ir_results(paper, args.year)
                if i == 0:
                    dict2["overviewpapers"].append(key)
                else:
                    dict2["participantpapers"].append(key)
                i += 1
            dict2["link"] = ""
            dict["tasks"].append(dict2)
    return dict



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('origin', type=str, nargs='?', default="trec",  # trec #ntcir #ceur
                        help='origin of the proceeding(currently trec or ceur)')

    parser.add_argument('proceeding_url', type=str, nargs='?', default="D:/eclipse/webscrapersT/src/htmls/Alphabetical Index of TREC-9 Papers by Task_Track.html",
                        # http://ceur-ws.org/Vol-2696/ , "https://trec.nist.gov/pubs/trec30/xref.html" , https://research.nii.ac.jp/ntcir/workshop/OnlineProceedings14/NTCIR/toc_ntcir.html
                        help='url to the proceeding')

    parser.add_argument('proceeding_name', type=str, nargs='?', default="TREC",  # TREC #FIRE #CLEF #NTCIR #MediaEval
                        help='name of the proceeding (curr. TREC/CLEF/FIRE/MediaEval/NTCIR)')

    parser.add_argument('year', type=int, nargs='?', default="2000",
                        help='year of the proceeding')

    parser.add_argument('online', type=bool, nargs='?', default=False,  # True
                        help='true is origin is from the web, false if its a local .html file')

    args = parser.parse_args()

    if args.origin == "trec":
        tasknames, taskpapers = get_paper_from_trec(args.proceeding_url)
    if args.origin == "ntcir":
        tasknames, taskpapers = get_paper_from_ntcir(args.proceeding_url)
    if args.origin == "ceur":
        if args.proceeding_name == "MediaEval":
            tasknames, taskpapers = get_paper_from_ceur_medival(args.proceeding_url)
        else:
            tasknames, taskpapers = get_paper_from_ceur(args.proceeding_url)

    print(tasknames)
    print(taskpapers)

    conf = args.proceeding_name
    dict = create_dict(tasknames, taskpapers, conf)
    print(dict)
    outfile = "shared-tasks_tmp.json"
    with open(outfile, "w") as file:
        json.dump(dict, file)
