import fitz
import argparse
import os


def run(pdfpath, paperpath, contentstart, contentend):

    with fitz.open(pdfpath) as pdf:

        pagenumbers = []
        papernames = []
        for page in pdf.pages(contentstart, contentend):

            for link in page.get_links():
                lr = link.get("from")
                padding = 10
                tmp = (page.get_textbox(lr + (-padding, -padding, padding, padding)))
                if not tmp in papernames:
                    papernames.append(tmp)
                pagenumbers.append(int(link.get("page")))

        pagenumbers = list(dict.fromkeys(pagenumbers))

        realpapernames = []
        papername = ""
        for str in papernames:
            if str.isnumeric():
                realpapernames.append(papername)
                papername = ""
            else:
                papername += str.replace(". ", "").replace("\n"," ").replace("\\"," ").replace("/"," ").replace(":"," ").replace("*"," ").replace("|"," ").replace(">"," ").replace("<"," ").replace("?"," ").strip()



        for i in range(len(pagenumbers)-1):
            paper = fitz.open()                 # new empty PDF
            paper.insert_pdf(pdf, from_page=pagenumbers[i], to_page=pagenumbers[i+1]-1)
            paper.save(paperpath + "/" + realpapernames[i] + ".pdf")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('pdfpath', type=str, nargs='?', default="goos21-overview-of-lilas-2021-living-labs-for-academic-search.pdf",
                        help='path to pdf')
    parser.add_argument('paperpath', type=str, nargs='?', default="paper",
                        help='path to the papers')
    parser.add_argument('contentstart', type=int, nargs='?', default="18",
                        help='start of the table of contents')
    parser.add_argument('contentend', type=int, nargs='?', default="21",
                        help='end of the table of contents')

    args = parser.parse_args()

    if args.pdfpath[-4:] !=".pdf":
        print("please input a .pdf file")

    if not os.path.isdir(args.paperpath):
        os.mkdir(args.paperpath)

    run(args.pdfpath, args.paperpath, args.contentstart, args.contentend)
