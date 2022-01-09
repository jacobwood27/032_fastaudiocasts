import os
import xml.etree.ElementTree as ET

pods = [
    ("ezra",   "1.8", "https://feeds.simplecast.com/82FI35Px"),
    ("lex",    "1.8", "https://lexfridman.com/feed/podcast/"),
    ("80k",    "1.8", "https://feeds.feedburner.com/80000HoursPodcast"),
    ("rspeak", "1.8", "https://rationallyspeakingpodcast.libsyn.com/rss"),
    ("tyler",  "1.8", "https://cowenconvos.libsyn.com/rss"),
    ("econ",   "1.8", "http://files.libertyfund.org/econtalk/EconTalk.xml"),
    ("mscape", "1.8", "https://rss.art19.com/sean-carrolls-mindscape"),
]

feed = ET.parse("feed.xml")
feed_root = feed.getroot()
feed_chan = feed_root.find('./channel')

for pod in pods:
    os.system("wget " + pod[2] + " -O raw.xml")
    
    tree = ET.parse("raw.xml")
    root = tree.getroot()
    os.remove("raw.xml")
        
    ep = root.find('./channel/item')
    ep_id = ep.find('guid').text
    ep_title = ep.find('title').text
    ep_audio = ep.find('enclosure').attrib['url']
    ep_date  = ep.find('pubDate').text
    
    file_name = "".join([c for c in ep_title if c.isalpha() or c.isdigit()]).rstrip() + ".mp3"
    full_file = os.path.join("audio", pod[0], file_name)
    
    print("Title: " + ep_title)
    print("ID: " + ep_id)
    print("filename: " + file_name)
    
    if not os.path.exists(full_file):
        # Get the new episode audio and save it
        os.system("wget \"" + ep_audio + "\" -O raw.mp3")
        os.system("ffmpeg -i raw.mp3 -filter:a \"atempo=" + pod[1] + "\" -q:a 6 " + full_file) #quality 6 seems to be a good middle ground https://trac.ffmpeg.org/wiki/Encode/MP3  at ~115kb/s we should be able to store a 2 hour audio file without exceeding 100MB LFS [100E6/(115E3/8)/60/60=1.93]
        os.remove("raw.mp3")
        
        #Make the new XML item element
        new_item = ET.Element('item')
        
        new_title = ET.Element('title')
        new_title.text = pod[0] + " " + ep_title
        
        new_enclosure = ET.Element('enclosure', 
                                   url="https://raw.githubusercontent.com/jacobwood27/032_fastaudiocasts/main/audio/" + pod[0] + "/" + file_name, 
                                   length=str(os.path.getsize(full_file)), 
                                   type="audio/mpeg")

        new_guid = ET.Element("guid")
        new_guid.text = ep_id + "_1.8x"
        
        new_pubdate = ET.Element("pubDate")
        new_pubdate.text = ep_date
        
        new_item.append(new_title)
        new_item.append(new_enclosure)
        new_item.append(new_guid)
        new_item.append(new_pubdate)
        
        #Add it to feed.xml
        feed_chan.insert(3, new_item) #after title, language, and description
        feed.write('feed.xml')
    
