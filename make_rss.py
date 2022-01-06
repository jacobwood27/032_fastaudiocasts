import os
import xml.etree.ElementTree as ET

pods = [
    "https://feeds.simplecast.com/82FI35Px"
]

for pod in pods:
    # os.system("wget " + pod + " -O raw.xml")
    
    tree = ET.parse("raw.xml")
    root = tree.getroot()
    latest_audio = root.find('./channel/item/enclosure').attrib['url']
    
    os.system("wget \"" + latest_audio + "\" -O raw.mp3")
    os.system("ffmpeg -i raw.mp3 -filter:a \"atempo=1.7\" -q:a 100 fast.mp3")
    