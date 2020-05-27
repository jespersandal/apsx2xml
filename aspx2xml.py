import os
import sys
import re
import shutil
import io

def stripaspx(filestring):
    aspxstring = filestring
    xmlstring = ''

def getfilelist():
    filelist = []
    if len(sys.argv) < 2:
        cwd = os.getcwd()
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith('.aspx'):
                    filelist.append(os.path.join(root, file))
    return filelist

def gettitle(filestring):
    titleregex = re.compile(r'(\<title\>)([\w\s\-\?\:]+)(\<\/title\>)')
    title = titleregex.search(filestring)
    if title is None:
        title = 'No title found\n'
        return title
    return title.group(2)

def getlead(filestring):
    leadregex = re.compile(r'(\<mso\:Comments\smsdt\:dt\=\"string\"\>)(.+)(\<\/mso\:Comments\>)', re.DOTALL)
    lead = leadregex.search(filestring)
    if lead is None:
        lead = 'No lead found\n'
        return lead
    return lead.group(2)

def getpublished(filestring):
    publishedregex = re.compile(r'(\<mso\:PublishingStartDate\smsdt\:dt\=\"string\"\>)(.+)(\<\/mso\:PublishingStartDate\>)', re.DOTALL)
    published = publishedregex.search(filestring)
    if published is None:
        published = 'No date found\n'
        return published
    publisheddate = published.group(2)
    return publisheddate

def getkeywords(filestring):
    keywordsregex = re.compile(r'(\<mso\:MetaKeywords\smsdt\:dt\=\"string\"\>)(.+)(\<\/mso\:MetaKeywords\>)', re.DOTALL)
    keywords = keywordsregex.search(filestring)
    if keywords is None:
        keywords = 'No date found\n'
        return keywords
    keywordstr = keywords.group(2)
    return keywordstr

def getcontent(filestring):
    contentregex = re.compile(r'(\<mso\:Content\smsdt\:dt\=\"string\"\>)(.+)(\<\/mso\:Content\>)', re.DOTALL)
    content = contentregex.search(filestring)
    if content is None:
        content = 'No content found\n'
        return content
    contentstr = content.group(2)
    # contentstr = fixHTML(contentstr)
    return contentstr

def fixHTML(xmltext):
# Fixing the HTML-tags creates an invalid XML-file.
# It may be better to fix it on import.
    ltregex = re.compile(r'\&lt\;')
    gtregex = re.compile(r'\&gt\;')
    quotregex = re.compile(r'\&quot\;')
    xmltext = ltregex.sub('<', xmltext)
    xmltext = gtregex.sub('>', xmltext)
    xmltext = quotregex.sub('"', xmltext)
    return xmltext

def convertfiles():
    filelist = getfilelist()
    for files in filelist:
        if os.path.splitext(files)[1] != '.aspx':
            continue
        else:
            openfile = io.open(files, mode='r', encoding='utf-8')
            filecontent = openfile.read()
            openfile.close()
            title = gettitle(filecontent)
            keywords = getkeywords(filecontent)
            lead = getlead(filecontent)
            publisheddate = getpublished(filecontent)
            content = getcontent(filecontent)
            xmlstring = '<?xml version="1.0" encoding="UTF-8"?>\n' + '<article>\n' + '<date>' + publisheddate + '</date>\n' + '<keywords>' + keywords + '</keywords>\n' + '<title>' + title + '</title>\n' + '<manchet>' + lead + '</manchet>\n' + '<htmlcontent>' + content + '</htmlcontent>\n' + '</article>\n'
            xmlfilename = os.path.splitext(files)[0] + '.xml'
            xmlfile = io.open(xmlfilename, mode='w', encoding='utf-8')
            xmlfile.write(xmlstring)
            xmlfile.close()

# searchfiles()
convertfiles()
