# WordMapGenerator
Word Map Generator is a program that uses the Tagul Word Cloud API to generate word maps. The first function 
(get_region_word_clouds) calls the Tagul API to generate SVG word clouds in the shapes of the regions that comprise 
a country or set of countries. Then, the second function (get_word_map) resizes the regional SVG word clouds to 
geographic scale and overlays an SVG map with them.

This program currently supports maps of the United States, United Kingdom, Australia and Latin America (Argentina, 
Bolivia, Brazil, Chile, Colombia, Costa Rica, Dominican Republic, Ecuador, El Salvador, Guatemala, Honduras, Mexico,
Nicaragua, Panama, Paraguay, Peru, Uruguay, and Venezuela).

# Setup

Ensure you have the xmlrpclib and zlib libraries installed. You will also need to register for a premium account on 
tagul.com for API access. Replace the USERNAME and PASSWORD in GetWordMap.get_region_word_clouds with your credentials. 
