import xml.etree.ElementTree as ET
from pprint import pprint

def xml2py(node):
    """
    convert xml to python object
    node: xml.etree.ElementTree object
    """

    name = node.tag

    pytype = type(name, (object, ), {})
    pyobj = pytype()

    for attr in node.attrib.keys():
        setattr(pyobj, attr, node.get(attr))

    if node.text and node.text != '' and node.text != ' ' and node.text != '\n':
        setattr(pyobj, 'text', node.text)

    for cn in node:
        if not hasattr(pyobj, cn.tag):
            setattr(pyobj, cn.tag, [])
        getattr(pyobj, cn.tag).append(xml2py(cn))

    return pyobj

tree = ET.parse('Small_artists.xml')
root = tree.getroot()

"""
{'aliases': [<__main__.aliases object at 0x101787390>],
 'data_quality': [<__main__.data_quality object at 0x1017871d0>],
 'id': [<__main__.id object at 0x1017870b8>],
 'name': [<__main__.name object at 0x1017870f0>],
 'namevariations': [<__main__.namevariations object at 0x101787240>],
 'profile': [<__main__.profile object at 0x101787160>],
 'realname': [<__main__.realname object at 0x101787128>],
 'text': '\n\t\t'}
{'aliases': [<__main__.aliases object at 0x1017876d8>],
 'data_quality': [<__main__.data_quality object at 0x101787668>],
 'id': [<__main__.id object at 0x101787470>],
 'members': [<__main__.members object at 0x101787828>],
 'name': [<__main__.name object at 0x101787588>],
 'profile': [<__main__.profile object at 0x1017875f8>],
 'text': '\n\t\t'}
[Finished in 0.1s]
"""

"""
<artist>
		<id>19</id>
		<name>Sound Associates</name>
		<profile></profile>
		<data_quality>Needs Vote</data_quality>
		<aliases>
			<name id="3653">Daz Saund &amp; Ben Tisdall</name>
			<name id="7507">Housewerk</name>
		</aliases>
		<members>
			<id>6482</id>
			<name id="6482">Ben Tisdall</name>
			<id>15867</id>
			<name id="15867">Daz Saund</name>
		</members>
	</artist>
"""

class Artist:

	# id = int()
	# name = str()
	# profile = str()
	# data_quality = str()
	# aliases = [
	# 	{
	# 	"name": str(),
	# 	"id"; int()
	# 	}
	# ]
	# members = [
	# 	{
	# 	"name": str(),
	# 	"id": str()
	# 	}
	# ]

	def __init__(self):
		pass

for child in root:
	artist = xml2py(child)
	
	id = artist.id[0].text
	print(id)



# for child in root:
# 	for child_2 in child:
# 		print(child_2)

