import sys
import glob
import xml.etree.ElementTree as ET

ET.register_namespace('', "http://www.w3.org/2000/svg")
ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")

def change_font(path, font_family):
    for file in glob.glob(path):
        tree = ET.parse(file)
        root = tree.getroot()

        for text in root.iter():
            if text.get('font-family'):
                text.set('font-family', font_family)

        tree.write(file, 'UTF-8')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        exit(1)

    path = args[1]
    font_family = args[2]
    change_font(path, font_family)

