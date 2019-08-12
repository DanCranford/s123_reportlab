# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:00:55 2019

@author: dcraw
"""

#class feature_package(object):
#    def __init__(self, layer, sql_query):
#        self.main_fset = layer.query(sql_query)
#        self.fields_main = self.main_fset.fields
#        self.fm_main = {}
#        for field in self.fields_main:
#            self.fm_main[field['name']]=field['alias']
#        
#        self.attributes = self.main_fset.features[0].attributes
#        self.geometry = self.main_fset.features[0].geometry
#        
##        self.alias_attributes = [[self.fm_main[field],self.attributes['field']] for field in list(fm_main.keys())]
#        
#        if layer.properties.hasAttachments:
#            self.att_res = layer.attachments.search(sql_query)
#            
#            
#    def build_field_order(self):
#        att_alias = []
#        for field in list(self.fm_main.keys()):
#            att_alias.append([self.fm_main[field],self.attributes[field]])
#        return att_alias
#    
#    def grab_att_links(self):
#        return [info['DOWNLOAD_URL'] for info in self.att_res]


        
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












class base_featpacker(object):
    def __init__(self):
        self.main_fset = None
        self.fields_main = None
        self.fm_main = {}
        self.attributes = {}
        self.geometry = {}
        self.has_attachments = False
        self.has_related_tables = False
        self.att_res = None
        self.layer_name = None
        


class main_featpacker(base_featpacker):
    def __init__(self):
        base_featpacker.__init__(self)
        self.relationships = []
        self.related_data = []
        self.exclude_fields = []
    def __str__(self):
        return(str(self.attributes))
        
    def build_field_order(self, simplify = True):
        att_alias = []
        
        if simplify:
            list_fields = [field for field in list(self.fm_main.keys()) if field not in self.exclude_fields]
        else:
            list_fields = [field for field in list(self.fm_main.keys())]
        for field in list_fields:
            att_alias.append([self.fm_main[field],self.attributes[field]])
        return att_alias
    
    def grab_att_links(self):
        return [info['DOWNLOAD_URL'] for info in self.att_res]
        
class related_set(object):
    def __init__(self):
        self.layer_name = None
        self.features = []
        self.has_attachments = False
        self.fields = []
        self.exclude_fields = []
    
    def return_fset(self):
        try:
            from arcgis.features import FeatureSet
            fset =  FeatureSet(self.features)
            fset.fields = self.fields
            return fset
        except:
            raise Exception ('You might not have the arcgis module')
    def return_sdf(self, simplify = True):
        try:
            from arcgis.features import FeatureSet
            if simplify:
                out_fields = [field['name'] for field in self.fields if field['name'] not in self.exclude_fields]
            else:
                out_fields = [field['name'] for field in self.fields]
            return FeatureSet(self.features).sdf[out_fields]
        except:
            raise Exception ('You might not have the arcgis module')
        
        
        
        
class Utils(object):
    def __init__(self):
        pass
    
    @staticmethod
    def from_layer(layer, sql_query):
        # return a list of Dave_feature
#        dave_feature_set = []
#        feature_set = layer.query(sql_query)
#        for feature in feature_set:
#            _feature = Dave_feature(feature)
#            dave_feature_set.append(_feature)
        
        temp_object = main_featpacker()
        temp_object.main_fset = layer.query(sql_query)
        if len(temp_object.main_fset)>1:
            raise Exception('More than 1 feature')
        temp_object.fields_main = temp_object.main_fset.fields
        temp_object.fm_main = {}
        for field in temp_object.fields_main:
            temp_object.fm_main[field['name']]=field['alias']
        
        temp_object.attributes = temp_object.main_fset.features[0].attributes
        temp_object.geometry = temp_object.main_fset.features[0].geometry
                
        if layer.properties.hasAttachments:
            temp_object.has_attachments = True
            temp_object.att_res = layer.attachments.search(sql_query)
        
        
        temp_object.layer_name = layer.properties.name
        if layer.container.properties.editorTrackingInfo['enableEditorTracking']:
            temp_object.exclude_fields+=dict(layer.properties.editFieldsInfo).values()
            temp_object.exclude_fields.append(layer.properties.objectIdField)
            temp_object.exclude_fields.append(layer.properties.globalIdField)
        if len(layer.properties.relationships)>0:
            temp_object.has_related_tables = True
            temp_object.relationships = layer.properties.relationships
            
            all_tab_layers = layer.container.layers+layer.container.tables
            
            
            for relater in temp_object.relationships:
                tempset = related_set()
                temp_rel_query = layer.query_related_records(temp_object.attributes[layer.properties.objectIdField],relater['id'])
                tempset.fields = temp_rel_query['fields']
                tempset.features = temp_rel_query['relatedRecordGroups'][0]['relatedRecords']
                
                for tab_layer in all_tab_layers:
                    if tab_layer.url.split('/')[-1]==str(relater['id']):
                        templayer = tab_layer
                
                
                if templayer.properties.hasAttachments:
                    tempset.has_attachments=True
                tempset.layer_name = templayer.properties.name
                if layer.container.properties.editorTrackingInfo['enableEditorTracking']:
                    tempset.exclude_fields+=dict(templayer.properties.editFieldsInfo).values()
                tempset.exclude_fields.append(templayer.properties.objectIdField)
                tempset.exclude_fields.append(templayer.properties.globalIdField)
                if 'parentglobalid' in [field['name'] for field in tempset.fields]:
                    tempset.exclude_fields.append('parentglobalid')
                
                temp_object.related_data.append(tempset)
        
        
        
        
        
        
        return temp_object
            
            

































