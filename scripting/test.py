import wget
import os
import PIL
from PIL import Image

monthDict = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}

def processDate(dc):
	dc[0]=''.join(i for i in dc[0] if i.isdigit())
	dc[1] = monthDict[dc[1]]
	return dc

#This lists all the comics in the archive
url="http://icrywhileusleep.webcomic.ws/archive/"
archivepage = wget.download(url)

comiclist = []

numComicsToDownload = 30

with open(archivepage) as f:
    for line in f:
		#all the comics are in a line in a table
		if line.find("<tr><td>") != -1:
			comic = {}
			#first is the number of the comic
			fromcomicnum = line[line.find("<tr><td>")+8:]
			aftercomicnum = fromcomicnum.find("</td><td>")
			#extract comic number here
			comicnum = fromcomicnum[:aftercomicnum]
			comic["num"] = comicnum
			#the next row will be the link to the comic itself
			afternumline = fromcomicnum[aftercomicnum+9:]
			#now find the title
			bracketindex = afternumline.find(">")
			endtitleindex = afternumline.find("</a>")
			#TODO: the ' s are html-escaped
			title = afternumline[bracketindex+1:endtitleindex]
			comic["title"] = title
			afterlinkindex = afternumline.find("</td><td>")
			afterlink = afternumline[afterlinkindex+9:]
			#now extract the date
			commaindex = afterlink.find(",")
			date = afterlink[:commaindex]
			if date.strip():
				datechunks = date.split()
				comic["date"] = processDate(datechunks)
				comiclist.append(comic)
				
#Hooray now we have a list of the comics with number, title and date... now to go to the page and get the alt text and image!
baseurl = "http://icrywhileusleep.webcomic.ws/comics/"

filestoremove = []

for comic in comiclist:
	#Go to the page for this comic and get the data
	if int(comic["num"]) < numComicsToDownload:
		comicurl=baseurl+comic["num"]
		comicpage = wget.download(comicurl)
		filestoremove.append(comicpage)
		comments = []	
	
		commentHeaderFound = 0
		with open(comicpage) as comicfile:
			for line in comicfile:
				
				if commentHeaderFound % 3 == 1:
					if line.find("<h4>") != -1:
						#This should be the date
						start = line.find("<h4>") + len("<h4>")
						end = line.find("</h4>")
						comment["date"] = line[start:end]
					if line.find("username") != -1:
						#this should be username
						start = line.find("username=") + len("username=")
						end = line.find("\"", start)
						comment["username"] = line[start:end]
					if line.find("<p>") != -1:
						#should be the comment itself
						start = line.find("<p>") + len("<p>")
						end = line.find("</p>")
						comment["comment"] = line[start:end]
						comments.append(comment)
						commentHeaderFound = commentHeaderFound + 1
				
				#find the part in the file that contains the goods
				if line.find("comicimagelink") != -1:
					linkstart = line[line.find("comicimagelink")+26:]
					quoteindex = linkstart.find("\"")
					#this tells us where the actual image is
					imagelink = linkstart[:quoteindex]
					comiclist[int(comic["num"])-1]["image"] = imagelink
					altstartindex = linkstart.find("title=")
					altendindex = linkstart.find("\" id=")
					#and here's alt-text!
					alt = linkstart[altstartindex+7:altendindex].replace(':', '&#58;')
					comiclist[int(comic["num"])-1]["alt"] = alt
				if line.find("class=\"commentheader") != -1:
					commentHeaderFound = commentHeaderFound + 1
					comment = {}
				
		comic["comments"] = comments
		
					
#now let's build a page!
directory = "../_posts/"
outdirectory = "../assets/comics/"
thumbnaildirectory = "../assets/thumbnails/"
for comic in comiclist:
	if int(comic["num"]) < numComicsToDownload:
		#get the actual image
		if comic.get("image") is not None:
			img = wget.download(comic.get("image"), out=outdirectory + comic.get("title").replace(" ", "-") + ".jpeg")
			
			#we need to create a thumbnail from the image
			basewidth = 300
			thumbnail = Image.open(img)
			wpercent = (basewidth / float(thumbnail.size[0]))
			hsize = int((float(thumbnail.size[1]) * float(wpercent)))
			thumbnail = thumbnail.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			img2 = thumbnail.crop((25, 25, 125, 125))
			img2.save(thumbnaildirectory + comic.get("title").replace(" ", "-") + ".jpeg")

			#year-month-day-title.md
			date = comic.get("date")
			title = directory + date[2] + "-" + date[1] + "-" + date[0] + "-" + comic.get("title") + ".md"
			post = open(title,"w+")
			post.write("---\n")
			post.write("layout: comic\n")
			post.write("title: " + comic.get("title") + "\n")
			post.write("alt: " + comic.get("alt") + "\n")
			post.write("image: " + img[len(outdirectory):] + "\n")
			commenttext = ', '.join(str(x) for x in comic.get("comments")) 
			post.write("comment: " + str(comic.get("comments")) + "\n")
#			post.write("comment: " + commenttext + "\n")

			post.write("---\n")
			
#clean up
os.remove("download.wget")
for f in filestoremove:
	os.remove(f)

#	comicimagelink"><img src="http://icrywhileusleep.webcomic.ws/images/comics/68/f55680efe4f141081cd7a239047a1c6c909113944.jpg" alt="Pop Quiz" title="Feel free to stay up all night thinking about your answer." id="comicimage" /></a></a></div>

#layout: comic
#title: Yarp
#alt: OK THIS IS THE ONE
#image: bad.jpeg
#comment: Here is the first one.	
