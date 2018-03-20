# metalink-chan
# version 1.01
#
# / i am not sure what i expected. /
#

# imports
from lxml.html.clean import Cleaner
import os, sys, shutil, getopt, re, argparse, codecs, os.path

# vars
html = ""
filename = ""

# argument parse
parser = argparse.ArgumentParser(description="Strips off printable versions of metalink " + \
                                             "articles of unnecessary stuff.")
parser.add_argument("-f","--file", help="metalink article name",required=True)
args = parser.parse_args()
filename = args.file

# file check
if not os.path.isfile(filename) and not os.access(sys.argv[1], os.R_OK):
    print "WARNING - Couldn't find specified file!"
    sys.exit(1)
elif not os.path.exists('original'):
    print 'Creating original directory for backups...'
    os.makedirs('original')

# cleaner
cleaner = Cleaner(page_structure=False)
cleaner.remove_tags = ["span"]
cleaner.kill_tags = ["script","img","style"]


# original file conversion
original = codecs.open(filename,"r","cp866")
for line in original:
    line = re.sub(r"[^\x00-\x7F]+","",line)
    #if "&nbsp;" in line:
        #line = re.sub(r"&nbsp;", "", line)
    if "&reg;" in line:
        line = line.replace("&reg;","")
    number = re.search(r"<span style=\"display:none\">\d+</span>", line)
    if number:
        line = re.sub(r"<span style=\"display:none\">\d+</span>", "", line)
    footer = re.search(r"Didn't find what you are looking for\?", line)
    if footer:
        line = re.sub(r"Didn't find what you are looking for\?", "", line)
    header = re.search(r"Copyright \(c\) 20(\d){2}, Oracle\. All rights reserved\.", line)
    if header:
        line = re.sub(r"Copyright \(c\) 20(\d){2}, Oracle\. All rights reserved\.", "", line)
    html = html+line
original.close()
shutil.move(filename,'original\\'+filename)

# first temp file
temp = codecs.open("tmp_"+filename,"w","utf-8")
temp.write(cleaner.clean_html(html))
temp.close()

# second temp file and beautification
new_temp = open("tmp_"+filename,"r")
doc = open("Metalink_"+filename,"w")
for line in new_temp:
    if "<title>" in line:
        line = line.replace("</title>","</title>" + \
                            # meta 
                            "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />" + \
                            # style start
                            "<style>" + \
                            # display none
                            "#d1\:\:skip, #kmPgTpl\:r1\:0\:Headpgl, #kmPgTpl\:r1\:0\:pgl29, #kmPgTpl\:sd_r1\:0\:dv_rDoc\:0\:Headpgl, #kmPgTpl\:sd_r1\:0\:pgl3 {display: none;}" + \
                            # font
                            "p,b {font-size: 10pt;} " + \
                            # parts
                            "body {font-family: Segoe UI; margin-left: 5%; margin-right: 5%; } " + \
                            "hr { background-color: #ccc; border: 0px; color: #ccc; height: 1px; }" + \
                            "a { color: #105CB6; text-decoration: none; font-size: 11pt; }" + \
                            "a:hover, a:focus { color: #105CB6; }" + \
                            "a:active { color: #105CB6; }" + \
                            "div.kmcodeblock { background-color:#EEF3F7; overflow:auto; border-width:1px; border-style:solid; border-color:#C4D1E6; padding:0.5em; margin:0px; margin-top:5px; " + \
                                              "font-family:\"Courier New\",Courier,monospace; font-size:90%; xborder-width:0px; background-color: #E0EAF1; } " + \
                            ".kmnotebox { background-color:#FEFCEE; border: 2px solid #c1a90d; padding: 10px; border: 0px; background-color: #FFF9D7; border: 1px solid #c1a90d; } " + \
                            "h1.km { font-family: Arial, Helvetica, sans-serif; font-size:120%; color: #333333; padding-top: 1em; } " + \
                            "h2.km { font-family: Arial, Helvetica, sans-serif; font-size:105%; color: #333333; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #c4d1e6; " + \
                                     "padding-top: 0.5em; font-size: 125%; background-color: #777773; color: #FFFFFF; text-transform: uppercase; padding-top: 6px; padding-bottom: 6px; padding-left: 8px; } " + \
                            "h3.km { font-family: Arial, Helvetica, sans-serif; font-size:105%; font-weight: bold; color: #333333; padding-top: 0.5em; } " + \
                            "h4.km { font-family: Arial, Helvetica, sans-serif; font-size:101%; font-weight: bold; font-style:italic; color: #000088; padding-top: 0.5em; } " + \
                            "h5.km { font-family: Arial, Helvetica, sans-serif; font-size:101%; font-weight: bold; font-style:italic; color: #666666; padding-top: 0.5em; } " + \
                            "table.km { border-top-width: 1px; border-left-width: 1px; border-top-style: solid; border-left-style: solid; border-top-color: #c4d1e6; border-left-color: #c4d1e6; } " + \
                            "td.km { border-right-width: 1px; border-bottom-width: 1px; border-right-style: solid; border-bottom-style: solid; border-right-color: #c4d1e6; border-bottom-color: #c4d1e6; padding: 4px; vertical-align: top; } " + \
                            "th.km { border-right-width: 1px; border-bottom-width: 1px; border-right-style: solid; border-bottom-style: solid; border-right-color: #c4d1e6; border-bottom-color: #c4d1e6; padding: 4px; " + \
                                    "background-color: #dee6ef; font-weight: bold; text-align: left; vertical-align: top; } " + \
                            ".kmhidetext { font-family: Arial, Helvetica, sans-serif; font-size:103%; color: #333333; } " + \
                            "pre.km, code.km { font-family:\"Courier New\",Courier,monospace; font-size:90%; white-space: -moz-pre-wrap; white-space: -pre-wrap; white-space: -o-pre-wrap; white-space: pre-wrap; word-wrap: break-word; }" + \
                            "div.kmindent1 { display: block; padding-left: 40px; } " + \
                            "div.kmindent2 { display: block; padding-left: 80px; } " + \
                            "span.kmfixedwidthfont { font-family:\"Courier New\",Courier,monospace; } " + \
                            "h2.awiz { font-family: Arial, Helvetica, sans-serif; font-size:105%; color: #333333; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #c4d1e6; } " + \
                            "h3.awiz { font-family: Arial, Helvetica, sans-serif; font-size:103%; color: #333333; } " + \
                            "pre.awiz, code.awiz { font-family:\"Courier New\",Courier,monospace; font-size:90%; } " + \
                            ".bugOutputLabel { font-family: Helvetica, sans-serif; font-size:130%; font-weight: bold; color: #333333; } " + \
                            ".bugOutputText{ font-family: Helvetica, sans-serif; font-size:130%; color: #333333; } " + \
                            ".kmBrowserFavOText { font-family: Tahoma, Verdana, Helvetica, sans-serif; font-weight:normal; font-size:11px; } " + \
                            ".kmBrowserFavOTextSmall { font-family: Tahoma, Verdana, Helvetica, sans-serif; font-weight:normal; font-size:9px; } " + \
                            ".kmBrowserFavLink{ color:Navy; text-decoration:none; } " + \
                            ".kmDialogDutton_Highlight {font-size:small; background-color:rgb(255,255,180); border-color:Red; border-style:solid;} " + \
                            ".kmDialogDutton_Highlight:hover {font-size:small; background-color:rgb(255,255,100); border-color:Red; border-style:solid;} " + \
                            ".kmDialogDutton_Highlight:focus {font-size:small; background-color:rgb(255,255,100); border-color:Red; border-style:solid;} " + \
                            ".searchIconImage { margin-left: -38px; } " + \
                            ".kmContent img { max-width: 100%; } " + \
                            ".kmDocVisibilityInt { color:rgb(238,0,0); font-weight: bold; } " + \
                            ".kmDocVisibilityExt { color:Black; } " + \
                            ".kmDocBorderInternal { background-color:White; position:static; border-color:rgb(238,0,0); border-style:solid; padding-left: 5px; } " + \
                            ".kmDocBorderExternal { background-color:White; position:static; } " + \
                            # style end
                            "</style>")
    if "<p></p>" in line:
        line = re.sub("<p></p>", "", line)
    doc.write(line)
new_temp.close()
doc.close()
os.remove("tmp_"+filename)
if os.path.isfile("Metalink_"+filename):
    print "Done! Output file: \"Metalink_"+filename+"\""
else:
    print "WARNING - Converted article wasn't created."
    sys.exit(1)
