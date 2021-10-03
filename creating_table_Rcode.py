from lxml import objectify
import pandas as pd

# создание df Rcode
def createTableRcode():
    root_node = (objectify.parse('http://www.cbr.ru/scripts/XML_val.asp?d=0')).getroot()
    data = []
    for tag in root_node.findall('Item'):
        data.append([tag.find("Name").text, tag.find("EngName").text, tag.find("ParentCode").text])
    df_Rcode = pd.DataFrame(data)
    df_Rcode.columns = ['Name', 'EngName', 'Rcode']
    df_Rcode.to_csv('file1.csv')


createTableRcode()
