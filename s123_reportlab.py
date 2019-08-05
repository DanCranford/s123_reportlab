# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:00:55 2019

@author: dcraw
"""

class s123_package():
    def __init__(self, layer, sql_query):
        self.main_fset = layer.query(sql_query)
        self.fields_main = self.main_fset.fields
        self.fm_main = {}
        for field in self.fields_main:
            self.fm_main[field['name']]=field['alias']
        
        self.attributes = self.main_fset.features[0].attributes
        self.geometry = self.main_fset.features[0].geometry
        
#        self.alias_attributes = [[self.fm_main[field],self.attributes['field']] for field in list(fm_main.keys())]
        
        if layer.properties.hasAttachments:
            self.res = layer.attachments.search(sql_query)
            
            
    def build_field_order(self):
        att_alias = []
        for field in list(self.fm_main.keys()):
            att_alias.append([self.fm_main[field],self.attributes[field]])
        return att_alias


def canvas_it_up(att_data, pdf_path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    canvas = canvas.Canvas(pdf_path, pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)
    
    x = 30
    y = 750
    
    for pair in att_data:
        canvas.drawString(x, y, str(pair[0]))
        canvas.drawString(x+100, y, str(pair[1]))
        y-=15
    
    canvas.save()
        


import arcgis

org = 'https://wevm.maps.arcgis.com'
username = 'WEVMAPS'
password = 'ckd3sons'

GIS = arcgis.GIS(org,username,password)

item_survey = arcgis.gis.Item(GIS,'cf9e8f3bf6414a08944d0fa29ae736b6')

lyr_main = item_survey.layers[0]

sql_query = "OBJECTID = 5"

mypack = s123_package(lyr_main,sql_query)



testfile = r"C:\Users\dcraw\Desktop\test1.pdf"


import reportlab.platypus as platypus
from reportlab.lib.styles import getSampleStyleSheet

doc = platypus.SimpleDocTemplate(testfile)
style_sheet = getSampleStyleSheet()
p1 = platypus.Paragraph('''Check This shit out /n I think there needs to be html in here''', style_sheet['BodyText'])
table = platypus.Table(mypack.build_field_order())
image = platypus.Image(mypack.res[0]['DOWNLOAD_URL'])
doc.build(p1,table,image)



