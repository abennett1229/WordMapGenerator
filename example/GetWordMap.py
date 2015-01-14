import os
from datetime import date
import xmlrpclib
import zlib
from FileFunctions import file_to_matrix

#Get individual word clouds for a list of regions and corresponding input files
#Theme and Hex code lists are optional for color coding words according to broader themes they're assigned to
def get_region_word_clouds(my_country,region_list,theme_list,hex_code_list):
        #Define API endpoint and user credentials
        API_ENDPOINT = "https://tagul.com:8889/api"
        USERNAME = "xxxxxx";
        PASSWORD = "xxxxxx";
        for my_region in region_list:
                #Define the template xml file for the region
                xml_content_template_filename = 'xml/%s/%s.xml' % (my_country,my_region)
                #Define the xml string we will be appending to the template content
                xml_string =  "<tags>" + '\n'
                #Define xml filename to write modified template content to
                xml_filename = str(date.today()).replace('-','') + "_" + my_region + ".xml"
                xml_file = open(xml_filename,'w')
                #Store input file as a matrix
                #Input file should have these columns: 1)word - required, 2)value - required, 3)word theme - optional, 4)word url - optional
                input_filename = my_region + '_data.txt'
                mx_word_theme_value = file_to_matrix(input_filename)
                #Required list of words and dictionary of values
                word_list = []
                value_dict = {}
                #Optional dictionaries of word-theme pairs and url's
                theme_dict = {}
                url_dict = {}
                #Iterate through matrix to create lists and dictionaries
                for row in mx_word_theme_value:
                        my_word = row[0]
                        my_value = row[1]
                        my_theme = row[2]
                        my_url = row[3]
                        word_list.append(my_word)
                        value_dict[my_word] = my_value
                        theme_dict[my_word] = my_theme
                        url_dict[my_word] = my_url
                word_list = list(set(word_list))
                #Iterate through word list to write the each xml tag
                for my_word in word_list:
                        #Look up word value in dictionary
                        my_word_value = value_dict[my_word]
                        #Optional hex code assignment to themes
                        my_theme = theme_dict[my_word]
                        i = theme_list.index(my_theme)
                        my_hex_code = hex_code_list[i]
                        #Optional url look up
                        my_word_url = url_dict[my_word]
                        #Write tag for the word
                        tag = '<tag weight="%s" color="%s" url="%s">%s</tag>' % (my_word_value,my_hex_code,my_word_url,my_word)
                        tag += '\n'
                        #Add tag to the xml string
                        xml_string += tag
                        #Once iteration is complete, append the full xml string to the template content and write to xml files
                        if word_list.index(my_word) == len(word_list) - 1:
                                xml_content_template = open(xml_content_template_filename)
                                xml_content = xml_content_template.read()
                                xml_content = xml_content.replace("<tags>",xml_string)
                                xml_file.write(xml_content)
                                xml_file.close()
                #Call tagul API to generate word cloud
                xmlrpcClient = xmlrpclib.ServerProxy(API_ENDPOINT)
                with open(xml_filename, "r") as file:
                        cloudXML = file.read()
                callMethod = xmlrpcClient.getSVG		
                cloud = callMethod ({'username': USERNAME,'password': PASSWORD},cloudXML)
                data = zlib.decompress(cloud.data)
                #Define svg filename and write region word cloud data to the file
                output_filename = my_region + ".svg"
                with open(output_filename, 'wb') as file:
                        file.write(data)
                        file.close()
        #Remove region xml files from directory
        for my_region in region_list:
                xml_filename = str(date.today()).replace('-','') + "_" + my_region + ".xml"
                os.remove(xml_filename)


#Combine individual region word clouds into a single map
def get_word_map(my_country,region_list):
        #Read in svg map template file
        template_map_filename = 'svg/%s_black_map.svg' % (my_country)
        template_map_file = open(template_map_filename)
        template_map_content = template_map_file.read()
        #Define output filename for word map
        output_map_filename = str(date.today()).replace('-','') + '_' + my_country + '_word_map.svg'
        output_map_file = open(output_map_filename,'w')
        #Define a string to represent all region word clouds to append to svg map template file
        wc_string = ' '
        #Define filename with coordinates for each region in the map
    	region_position_filename = 'txt/%s_region_positions.txt' % (my_country)
        #Store file as a matrix
    	mx_region_positions = file_to_matrix(region_position_filename)
        #Create dictionaries for region coordinates
        x_dict = {}
        y_dict = {}
        w_dict = {}
        h_dict = {}
        for row in mx_region_positions:
                region = row[0]
                x = row[1]
                y = row[2]
                w = row[3]
                h = row[4]
                x_dict[region] = x
                y_dict[region] = y
                w_dict[region] = w
                h_dict[region] = h
        #Iterate through region list to look up region dimensions to replace dimensions in region svg content and append all updated content to svg map template
        for my_region in region_list:
                #Define region svg file
                region_filename = my_region + '.svg'
                region_file = open(region_filename)
                region_content = region_file.read()
                #Look up region coordinates in dictionaries
                region_width = w_dict[my_region] 
                region_height = h_dict[my_region] 
                region_x = x_dict[my_region]
                region_y = y_dict[my_region]
                #Replace dimensions in the input svg file content
                new_dimensions = ' width="%s" height="%s" x="%s" y="%s" ' % (region_width,region_height,region_x,region_y)
                old_dimensions = region_content.split('xmlns:t="http://www.tagul.com/schema"')[1]
                old_dimensions = old_dimensions.split('viewBox=')[0]
                region_content = region_content.replace(old_dimensions,new_dimensions)
                #Add updated region svg content to word cloud string
                wc_string += region_content
                #Once iteration is complete, append full word cloud string to the template svg map content and write to output map file
                if region_list.index(my_region) == len(region_list)-1:
                        output_map_content = template_map_content.replace('<?INSERT_WC_STRING?>',wc_string)
                        output_map_content = output_map_content.replace('<?xml version="1.0" encoding="UTF-8"?>','')
                        output_map_file.write(output_map_content)
                        output_map_file.close()
	                    #Remove region svg files from directory
        for my_region in region_list:
                region_filename = my_region + '.svg'
                os.remove(region_filename)
