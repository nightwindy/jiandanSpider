from urllib import request
import  os, re, threading, time

def getHtml(url) :
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = request.Request(url, headers=hdr)
    page = request.urlopen(req)
    html = page.read().decode('utf-8')
    return html

def filterComment(source) :
    pattern = r'begin comments([\s\S]*?)end comments'
    matchs = re.search(pattern, source)
    return matchs.group()

def filterThumbnail(source) :
    pattern = r'<img src="([\s\S]*?)\.jpg"'
    reobj = re.compile(pattern)
    result, number = reobj.subn('', source)
    return result

def downloadPicture(picurl, picpath, picname) :
    pic = request.urlopen(picurl)
    f = open(picpath + picname, 'wb')
    f.write(pic.read()) 
    f.close()
    print ('System: ' + picname + ' saved\n')

choice = 0
pagestart = 1
pageend = 100
ooover = 30
xxbelow = 100

if choice == 0 :
    dirname = "ooxx"
else :
    dirname = "pic"

path = os.getcwd() + "/" + dirname
isExists = os.path.exists(path)
if not isExists :
    print ('System: ' + path + " created")
    os.makedirs(path)
else :
    print ('System: ' + path + " exists")

initurl = "http://jandan.net/" + dirname + "/"

for pagenum in range(pagestart, pageend) :
    cururl = initurl + "page-" + str(pagenum)
    print ('Current url: ' + cururl)
    inithtml = getHtml(cururl)
    curhtml = filterComment(inithtml)

    pattern = r'<li id="comment-([\s\S]*?)</li>'
    reobj = re.compile(pattern)
    matchs = reobj.findall(curhtml)
    count0 = 0
    for match in matchs :
        count0 = count0 + 1
        match = filterThumbnail(match)

        oopattern = r'(?:<span class="tucao-like-container">)(?:[\s\S]*?)(?:<span>)(\d*?)(?:</span>)'
        xxpattern = r'(?:<span class="tucao-unlike-container">)(?:[\s\S]*?)(?:<span>)(\d*?)(?:</span>)'
        oo = re.search(oopattern, match).group(1)
        xx = re.search(xxpattern, match).group(1)

        picpattern = r'(?:href=")(//w[\s\S]*?)(.gif|.png|.jpg)'
        picobj = re.compile(picpattern)
        result = picobj.findall(match)

        count1 = 0
        for pic in result :
            if int(oo) > ooover and int(xx) < xxbelow:
                count1 = count1 + 1
                picurl = "http:"+pic[0] + pic[1]
                picpath = path + '/'
                picname = str(pagenum) + '_oo' + oo + '_xx' + xx + '_' + str(count0) + '_' + str(count1) + pic[1]

                print ('Infomation:')
                print ('Picture url: ' + picurl)
                print ('Picture path: ' + picpath)
                print ('Picture name: ' + picname)
                try :
                    downloadPicture(picurl, picpath, picname)
                except Exception as e :
                    print(e)