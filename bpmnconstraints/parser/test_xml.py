from xml.etree import ElementTree

xml = ElementTree.parse("examples/xml/Single XOR, trailing value.xml").getroot()

for elem in xml.iter():
    print(elem)
