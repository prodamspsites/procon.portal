# -*- coding: utf-8 -*-

PROJECTNAME = 'procon.portal'

# http://www.tinymce.com/wiki.php/Configuration:formats
TINYMCE_JSON_FORMATS = {'strikethrough': {'inline': 'span',
                                          'classes': 'strikethrough',
                                          'exact': 'true'},
                        'underline': {'inline': 'span',
                                      'classes': 'underline',
                                      'exact': 'true'}}

MONGODB_HOSTS = {
    'local': 'localhost',
    'dev': '10.20.26.12',
    'hom': '10.20.26.12',
    'prod': '10.20.26.12'
}
