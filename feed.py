import yaml
import xml.etree.ElementTree as xml_tree

#read file feed.yaml
with open('feed.yaml','r') as file:
    #load data in file feed.yaml to variable yaml_Data 
    yaml_data = yaml.safe_load(file)
    
    #create xml tree element with name rss_element
    rss_element = xml_tree.Element('rss', {'version':'2.0',
                                           'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
                                           'xmlns:content':'http://purl.org/rss/1.0/modules/content/'})
    
#add channel element to the tree
channel_element = xml_tree.SubElement(rss_element, 'channel')

#declare & intialize link prefix from yaml data link property
link_prefix = yaml_data['link']


#add sub elements to channel element from yaml data
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image',{'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix

xml_tree.SubElement(channel_element, 'itunes:category',{'text': link_prefix + yaml_data['category']})

#Create items individually in a dynamic way with enclosure property
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element,'item')
    xml_tree.SubElement(item_element,'title').text = item['title']
    xml_tree.SubElement(item_element,'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element,'description').text = item['description']
    xml_tree.SubElement(item_element,'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element,'pubDate').text = item['published']
    
    enclosure = xml_tree.SubElement(item_element,'enclosure',{
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

#Assign xmltree data
output_tree = xml_tree.ElementTree(rss_element)

#Create xml file named podcast with xml_tree data
output_tree.write('podcast.xml',encoding='UTF-8',xml_declaration=True)