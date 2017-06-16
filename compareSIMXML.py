import os
import packages.fileSearch as fileSearch
import packages.FolderFile as FolderFile
import lxml.etree
#import lxml.objectify
import io
from collections import defaultdict


def removeXmlNamespaces(dom):
    # http://wiki.tei-c.org/index.php/Remove-Namespaces.xsl
    xslt='''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="/|comment()|processing-instruction()">
        <xsl:copy>
          <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*">
        <xsl:element name="{local-name()}">
          <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="@*">
        <xsl:attribute name="{local-name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    </xsl:stylesheet>
    '''

    xslt_doc=lxml.etree.parse(io.BytesIO(xslt))
    transform=lxml.etree.XSLT(xslt_doc)
    dom=transform(dom)
    return dom

def getFiles(before, after):
    root_before = removeXmlNamespaces(lxml.etree.parse(before)).getroot()
    obj_xml_before =  lxml.etree.tostring(root_before, pretty_print=True)
    root_after = removeXmlNamespaces(lxml.etree.parse(after)).getroot()
    obj_xml_after =  lxml.etree.tostring(root_after, pretty_print=True)
    
    
    new_before = os.path.split(before)[1]
    new_after = os.path.split(after)[1]
    print new_before, new_after
    new_dir = os.path.join(os.path.split(before)[0],"noNameSpace")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    with open(os.path.join(new_dir,new_before), "w") as f:
        f.write(obj_xml_before)
    with open(os.path.join(new_dir,new_after), "w") as f:
        f.write(obj_xml_after)
    
    control_parameters = dict()
    component_parameters = dict()
    
    # before (controllerPositions)
    for control in root_before.iter('Control'):
        #print control.get('TypeOfControl'), control.get('Id')
        for result in control.iter('ControlGroup'):
            #print '  ', result.get('TypeOfGroup'), result.get('Id')
            for parameter in result:
                #print parameter.get('Name')
                name = parameter.get('Name')
                typeOfGroup = result.get('TypeOfGroup')
                result_ID = result.get('Id')
                if not result_ID:
                    result_ID = ''
                else:
                    result_ID = 'ID' #str(result_ID)
                control_ID = control.get('Id')
                if not control_ID:
                    control_ID = ''
                else:
                    control_ID = 'ID'
                try:
                    #control_parameters[name].append([control.get('TypeOfControl')+control.get('Id'), typeOfGroup+ID])
                    if not typeOfGroup+result_ID in control_parameters[name][control.get('TypeOfControl')+control_ID]:
                        control_parameters[name][control.get('TypeOfControl')+control_ID].append(typeOfGroup+result_ID)
                except:
                    #control_parameters[name] = dict({control.get('TypeOfControl')+control.get('Id'):list([typeOfGroup+ID])})
                    try:
                        control_parameters[name][control.get('TypeOfControl')+control_ID] = list([typeOfGroup+result_ID]) 
                    except:
                        control_parameters[name] = dict({control.get('TypeOfControl')+control_ID:list([typeOfGroup+result_ID])}) 
                #control_parameters.append(parameter.get('Name')) = control_parameters.get(parameter.get('Name'), []).append() 
    #for k,v in control_parameters.items():
    #    print k,v    

    # before (components)
    for component in root_before.iter('Component'):
        #print component.get('TypeOfComponent'), component.get('Id')
        for result in component.iter('ComponentGroup'):
            #print '  ', result.get('TypeOfGroup'), result.get('Id')
            for parameter in result:
                #print parameter.get('Name')
                name = parameter.get('Name')
                typeOfGroup = result.get('TypeOfGroup')
                result_ID = result.get('Id')
                if not result_ID:
                    result_ID = ''
                else:
                    result_ID = 'ID' #str(result_ID)
                component_ID = component.get('Id')
                if not component_ID:
                    component_ID = ''
                else:
                    component_ID = 'ID'
                try:
                    #component_parameters[name].append([component.get('TypeOfComponent')+component.get('Id'), typeOfGroup+ID])
                    if not typeOfGroup+result_ID in control_parameters[name][component.get('TypeOfComponent')+component_ID]:
                        control_parameters[name][component.get('TypeOfComponent')+component_ID].append(typeOfGroup+result_ID)
                except:
                    #control_parameters[name] = dict({component.get('TypeOfComponent')+component.get('Id'):list([typeOfGroup+ID])}) 
                    try:
                        control_parameters[name][component.get('TypeOfComponent')+component_ID] = list([typeOfGroup+result_ID]) 
                    except:
                        control_parameters[name] = dict({component.get('TypeOfComponent')+component_ID:list([typeOfGroup+result_ID])}) 
            #if result.get('TypeOfGroup') == 'Parameter' or result.get('TypeOfGroup') == 'Result':
            #    control_parameters
    #for k,v in control_parameters.items():
    #    print k,v   

    #control_keys = list(control_parameters)

    #print '---------------'
    # after (controllerPositions)
    for control in root_after.iter('Control'):
        #print control.get('TypeOfControl'), control.get('Id')
        for result in control.iter('ControlGroup'):
            #print '  ', result.get('TypeOfGroup'), result.get('Id')
            for parameter in result:
                #print parameter.get('Name')
                name = parameter.get('Name')
                typeOfGroup = result.get('TypeOfGroup')
                result_ID = result.get('Id')
                if not result_ID:
                    result_ID = ''
                else:
                    result_ID = 'ID' #str(result_ID)
                control_ID = control.get('Id')
                if not control_ID:
                    control_ID = ''
                else:
                    control_ID = 'ID'
                try:
                    #component_parameters[name].append([component.get('TypeOfControl')+component.get('Id'), typeOfGroup+ID])
                    if not typeOfGroup+result_ID in component_parameters[name][control.get('TypeOfControl')+control_ID]:
                        component_parameters[name][control.get('TypeOfControl')+control_ID].append(typeOfGroup+result_ID)
                except:
                    #component_parameters[name] = dict({control.get('TypeOfControl')+control.get('Id'):list([typeOfGroup+ID])})
                    try:
                        component_parameters[name][control.get('TypeOfControl')+control_ID] = list([typeOfGroup+result_ID]) 
                    except:
                        component_parameters[name] = dict({control.get('TypeOfControl')+control_ID:list([typeOfGroup+result_ID])}) 
                #except:
                    #component_parameters[name] = list([component.get('TypeOfControl')+component.get('Id'), typeOfGroup+ID])
    # after (components)
    for component in root_after.iter('Component'):
        #print component.get('TypeOfComponent'), component.get('Id')
        for result in component.iter('ComponentGroup'):
            #print '  ', result.get('TypeOfGroup'), result.get('Id')
            for parameter in result:
                #print parameter.get('Name')
                name = parameter.get('Name')
                typeOfGroup = result.get('TypeOfGroup')
                result_ID = result.get('Id')
                if not result_ID:
                    result_ID = ''
                else:
                    result_ID = 'ID' #str(result_ID)
                component_ID = component.get('Id')
                if not component_ID:
                    component_ID = ''
                else:
                    component_ID = 'ID'
                try:
                    #component_parameters[name].append([component.get('TypeOfComponent')+component.get('Id'), typeOfGroup+ID])
                    if not typeOfGroup+result_ID in component_parameters[name][component.get('TypeOfComponent')+component_ID]:
                        component_parameters[name][component.get('TypeOfComponent')+component_ID].append(typeOfGroup+result_ID)
                except:
                    #component_parameters[name] = dict({component.get('TypeOfComponent')+component.get('Id'):list([typeOfGroup+ID])})
                    try:
                        component_parameters[name][component.get('TypeOfComponent')+component_ID] = list([typeOfGroup+result_ID]) 
                    except:
                        component_parameters[name] = dict({component.get('TypeOfComponent')+component_ID:list([typeOfGroup+result_ID])}) 
                #except:
                #    component_parameters[name] = list([component.get('TypeOfComponent')+component.get('Id'), typeOfGroup+ID])
                
    #for k,v in component_parameters.items():
    #    print k,v
    #component_keys = list(component_parameters)
    try:
        writer, fh = FolderFile.createCsv(filename='output.csv', fieldnames=['parameter', 'before', 'after'], mode='wb')
        writer.writeheader()
        writer1, fh1 = FolderFile.createCsv(filename='output1.csv', fieldnames=['parameter', 'before', 'after'], mode='wb')
        writer1.writeheader()
        for k, v in control_parameters.items():
            if v != component_parameters.get(k, None):
                writer.writerow({'parameter': k, 'before': v, 'after':component_parameters.get(k, None)}) 
            else:
                writer1.writerow({'parameter': k, 'before': v, 'after':component_parameters.get(k, None)}) 
    finally:
        if fh:
            fh.close()
        if fh1:
            fh1.close()
    #for k, v in control_parameters.items():
    #    print k, '-----', v, '----->', component_parameters.get(k, None)
                
                
    # getting the attribute values
    #for param in root.iter('Parameter'):
    #    #print param.attrib
    #    parent = param.getparent().getparent()
    #    if parent.tag == 'Component':
    #        print parent.attrib.get('TypeOfComponent')
    #    if param.get('Name'):
    #        print ' --> ', param.tag, param.get('Name'), param.text # param.xpath('./@Name'), param.attrib['Name']
            


if __name__ == '__main__':
    before = r'/home/norman/Desktop/XML/lin/before.xml'
    after = r'/home/norman/Desktop/XML/lin/after.xml'
    getFiles(before=before, after=after)
