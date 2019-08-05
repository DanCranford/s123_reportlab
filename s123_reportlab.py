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
            self.att_res = layer.attachments.search(sql_query)
            
            
    def build_field_order(self):
        att_alias = []
        for field in list(self.fm_main.keys()):
            att_alias.append([self.fm_main[field],self.attributes[field]])
        return att_alias
    
    def grab_att_links(self):
        return [info['DOWNLOAD_URL'] for info in self.att_res]


#def canvas_it_up(att_data, pdf_path):
#    from reportlab.pdfgen import canvas
#    from reportlab.lib.pagesizes import letter
#    
#    canvas = canvas.Canvas(pdf_path, pagesize=letter)
#    canvas.setLineWidth(.3)
#    canvas.setFont('Helvetica', 12)
#    
#    x = 30
#    y = 750
#    
#    for pair in att_data:
#        canvas.drawString(x, y, str(pair[0]))
#        canvas.drawString(x+100, y, str(pair[1]))
#        y-=15
#    
#    canvas.save()
        
def generic_feature_report(feature_object, output_file):
    import reportlab.platypus as platypus
    from reportlab.lib.styles import getSampleStyleSheet
    
    elements = []
    doc = platypus.SimpleDocTemplate(output_file)
    style_sheet = getSampleStyleSheet()
    
    
    table = platypus.Table(feature_object.build_field_order())
    
    doc.build(elements)


