# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:00:55 2019

@author: dcraw
"""

class feature_package():
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


        
def generic_feature_report(feature_object, output_file):
    import reportlab.platypus as platypus
    from reportlab.lib.styles import getSampleStyleSheet
    
    elements = []
    doc = platypus.SimpleDocTemplate(output_file)
    style_sheet = getSampleStyleSheet()
    
#    pge_img = platypus.Image('https://www.cecsb.org/wp-content/uploads/2013/05/PGE-LOGO-1024x259.png')
#    elements.append(pge_img)
    elements.append(platypus.Paragraph('FEATURE REPORT',style_sheet['Heading1']))
    
    table = platypus.Table(feature_object.build_field_order())
    elements.append(table)
    
    if feature_object.att_res:
        for att in feature_object.att_res:
            elements.append(platypus.Image(att['DOWNLOAD_URL']))
    doc.build(elements)
    
    return(output_file)








































