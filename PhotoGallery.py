# -*- coding: iso-8859-1 -*-
# Copyright (c) 2003-2006 ETH Zurich, ID-TIM. Written by Benno Luthiger. All rights reserved.
# See also LICENSE.txt
# $Revision: 1.8 $
#
# Inspired by Marc's SilvaPhotoGallery Code Source (some code was copied from that product too).

import os

#Zope
from Globals import InitializeClass, package_home
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from OFS.Image import Image
from zope.interface import implements

#Silva
from Products.SilvaExternalSources.interfaces import IExternalSource
from Products.SilvaExternalSources.CodeSource import CodeSource
from Products.Silva import SilvaPermissions
from Products.Silva.helpers import add_and_edit

#Formulator
from Products.Formulator.Form import ZMIForm
from Products.Formulator.XMLToForm import XMLToForm

_help_info_s1_EN = u"""<strong>Help</strong><br />
Click on a photo to see large version or select a delay and click on &quot;Slideshow&quot; to start the slideshow. Click on the right (of left) half of the image to change to the next (previous) image. To close the image or stop the slideshow, click on the cross.<br />
Alternatively, you can use the following keys:<br />
<table>
  <tr><td>x&#160;</td><td>stop slideshow or close image</td></tr>
  <tr><td>c&#160;</td><td>stop slideshow or close image</td></tr>"""
_help_info_s2_EN = u"""<strong>Help</strong><br />
Click on a photo to see large version. Click on the right (of left) half of the image to change to the next (previous) image. To close the image click on the cross.<br />
Alternatively, you can use the following keys:<br />
<table>
  <tr><td>x&#160;</td><td>stop slideshow or close image</td></tr>
  <tr><td>c&#160;</td><td>stop slideshow or close image</td></tr>"""
_help_info_s3_EN = u"""Note: The manual change of pictures is disabled during slide show."""
_help_info_e_EN = u"""
  <tr><td>n&#160;</td><td>show next image</td></tr>
  <tr><td>p&#160;</td><td>show previous image</td></tr>
</table>"""
_help_info_s1_DE = u"""<strong>Hilfe</strong><br />
Klicken Sie auf ein Foto, um es in voller Grösse anzusehen oder wählen Sie ein Zeitintervall und klicken Sie auf &quot;Diaschau&quot;, um die Diaschau zu starten. Klicken Sie auf die rechte (oder linke) Bildhälfte, um auf das nächste (vorherige) Bild zu wechseln. Klicken Sie auf das Kreuz, um das Foto zu schliessen oder die Diaschau zu beenden.<br />
Alternativ können Sie die folgenden Tasten benutzen:<br />
<table>
  <tr><td>x&#160;</td><td>Diaschau beenden oder Foto schliessen</td></tr>
  <tr><td>c&#160;</td><td>Diaschau beenden oder Foto schliessen</td></tr>"""
_help_info_s2_DE = u"""<strong>Hilfe</strong><br />
Klicken Sie auf ein Foto, um es in voller Grösse. Klicken Sie auf die rechte (oder linke) Bildhälfte, um auf das nächste (vorherige) Bild zu wechseln. Klicken Sie auf das Kreuz, um das Foto zu schliessen.<br />
Alternativ können Sie die folgenden Tasten benutzen:<br />
<table>
  <tr><td>x&#160;</td><td>Foto schliessen</td></tr>
  <tr><td>c&#160;</td><td>Foto schliessen</td></tr>"""
_help_info_s3_DE = u"""Hinweis: Der manuelle Bildwechsel ist während der Diaschau abgeschaltet."""
_help_info_e_DE = u"""
  <tr><td>n&#160;</td><td>nächstes Foto zeigen</td></tr>
  <tr><td>p&#160;</td><td>vorheriges Foto zeigen</td></tr>
</table>"""

_translations = {
'hint':{'DE':u'Klicken Sie auf ein Foto, um es in voller Grösse anzusehen.', 'EN':u'Click on a photo to see large version.'},
'slideshow':{'DE':u'Diaschau', 'EN':u'Slideshow'},
'show_help':{'DE':u'Hilfe einblenden', 'EN':u'Show help'},
'help':{'DE':u'Hilfe', 'EN':u'Help'},
'help_info_s1':{'DE':_help_info_s1_DE, 'EN':_help_info_s1_EN},
'help_info_s2':{'DE':_help_info_s2_DE, 'EN':_help_info_s2_EN},
'help_info_s3':{'DE':_help_info_s3_DE, 'EN':_help_info_s3_EN},
'help_info_e':{'DE':_help_info_e_DE, 'EN':_help_info_e_EN}
}
_scripts = ['gallery_helper_scripts.js', 'lightbox.js', 'lightbox.css', 'photo_gallery.css']
_files = ['prototype.js', 'scriptaculous.js', 'effects.js']
_python = [] #['captions.xml']
_images = ['blank.gif', 'close.gif', 'loading.gif', 'minus.gif', 'next.gif', 'overlay.png', 'plus.gif', 'prev.gif']

pjoin = os.path.join
_phome = package_home(globals())
_folder = 'www'


def ustr(x):
    if type(x) == unicode:
        return x
    elif type(x) == str:
        return unicode(x, 'UTF-8')
    return str(x)

class PhotoGallery(CodeSource):
    """A photo gallery to show thumbnails and the original pictures within a Silva document.
    """

    implements(IExternalSource)
    meta_type = 'Silva Photo Gallery'
    security = ClassSecurityInfo()
    
    def __init__(self, id):
        CodeSource.inheritedAttribute('__init__')(self, id)
        self._script_id = 'view'
        self._data_encoding = 'UTF-8'
        self._description = self.__doc__
        
    def manage_afterAdd(self, item, container):
        self._set_form()
        self._set_views()

    security.declareProtected(SilvaPermissions.ChangeSilvaAccess,
                                'refresh')
    def refresh(self):
        """reload the form and pt"""
        if 'view' in self.objectIds():
            self.manage_delObjects(['view'])
        self._set_form()
        self._set_views()
        return 'refreshed form and pagetemplate'

    def _set_form(self):
        self.parameters = ZMIForm('form', 'Properties Form')
        f = open(pjoin(_phome, _folder, 'photo_gallery_form.form'))
        XMLToForm(f.read(), self.parameters)
        f.close()

    def _set_views(self):
        f = open(pjoin(_phome, _folder, 'photo_gallery_view.pt'))
        self._setObject('view', ZopePageTemplate('view', f.read()))
        f.close()
        
        self._add_images()
        self._add_dtml()
        self._add_file()
        self._add_python()
        
    def _add_images(self):
        for image in _images:
            f = open(pjoin(_phome, _folder, image), 'rb')
            self._setObject(image, Image(image, image, f))
            f.close()
            
    def _add_dtml(self):
        for script in _scripts:
            f = open(pjoin(_phome, _folder, script + '.dtml'), 'rb')
            text = f.read()
            f.close()
            self.manage_addDTMLMethod(script)
            getattr(self, script).manage_edit(text, '')
            
    def _add_file(self):
        for file in _files:
            f = open(pjoin(_phome, _folder, file), 'rb')
            text = f.read()
            f.close()
            self.manage_addFile(id=file, file=text, content_type='application/x-javascript')
            
    def _add_python(self):
        for script in _python:
            f = open(pjoin(_phome, _folder, script), 'rb')
            text = f.read()
            f.close()
            self.manage_addProduct['PythonScripts'].manage_addPythonScript(script)
            pscript = getattr(self, script)
            pscript.write(text)
            
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                'to_html')
    def to_html(self, *args, **kwargs):
        """render the photo gallery"""
        self.REQUEST.other['model'] = self
        try:
            return ustr(getattr(self, 'view')(**kwargs))
        except:
            import sys, traceback
            exc, e, tb = sys.exc_info()
            tbs = '\n'.join(traceback.format_tb(tb))
            del tb
            ret =  '%s - %s<br />\n\n%s<br />' % (exc, e, tbs)
            return ret
        
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'getPhotos')
    def getPhotos(self, model=None):
        """Returns a sorted list of photos found in the container.
        """
        try:
            if not model:
                model = self.REQUEST.model
            photos = model.get_container().objectValues('Silva Image')
        except:
            pass
        photos.sort(lambda x,y : cmp(x.getId(),y.getId()))
        return photos
    
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'getLanguage')
    def getLanguage(self):
        """The language of the document displaying the photos.
        """
        try:
            from Products.SilvaExtETHLayout.LanguageChecker import LanguageChecker
            model = self.REQUEST.model.get_content()
            language = LanguageChecker(model).get_current_language()
            if language in ['DE', 'EN']:
                return language
        except:
            pass
        return 'EN'
    
    security.declarePublic('getHint')
    def getHint(self, language):
        return _translations['hint'][language]
  
    security.declarePublic('getSlideShow')
    def getSlideShow(self, language, img_url, rel_attribute=""):
        html = """<select id="timeSelect">
    <option value="2000">2sec</option>
    <option value="5000" selected="selected">5sec</option>
    <option value="10000">10sec</option>
    <option value="30000">30sec</option>
  </select>
  <a id="slideshowStartLink" href="%s" rel="%s"></a>
  <input type="button" onclick="myLightbox.start(document.getElementById('slideshowStartLink')); slide=true; return false;" value="%s" />&#160;&#160;
  """
#slideshow_start();  
#<!-- <input type="button" onclick="showLightbox(document.getElementById('slideshowStartLink')); slide=true; return false;" value="-" />&#160;&#160; -->
        return html %(img_url, rel_attribute, _translations['slideshow'][language])
    
    security.declarePublic('getHelpButton')
    def getHelpButton(self, language):
        img_url = getattr(self, 'plus.gif').absolute_url()
        html = """<a class="nounderline" href="javascript:toggleElement('help')" title="%s"><img id="imghelp" src="%s" alt="plus" /></a><a href="javascript:toggleElement('help')" title="%s"><span>%s</span></a><br />"""
        show_help = _translations['show_help'][language]
        return html %(show_help, img_url, show_help, _translations['help'][language])
    
    security.declarePublic('getHelpInfo')
    def getHelpInfo(self, language, slide_show=0):
        html = """<div id="txthelp" style="display:none" class="expandable tablemargin">%s</div>"""
        help = _translations['help_info_s2'][language]
        if slide_show:
            help = _translations['help_info_s1'][language]
        help += _translations['help_info_e'][language]
        if slide_show:
            help += _translations['help_info_s3'][language]
        return html %help
        
    security.declarePublic('getCaption')
    def getCaption(self, caption):
        lenCaption = 42
        if len(caption) < lenCaption:
            return caption
        return caption[:lenCaption-3] + '...'
    
    security.declarePublic('pg_values_i18n')
    def pg_values_i18n(self, form, field_name):
        from Products.SilvaPhotoGallery import _form_translation
        return _form_translation.values_i18n(form, field_name)

InitializeClass(PhotoGallery)

manage_addPhotoGalleryForm = PageTemplateFile(
    "www/photoGalleryAdd", globals(), __name__='manage_addPhotoGalleryForm')

def manage_addPhotoGallery(context, id, title, REQUEST=None):
    """Add an Inline Viewer"""
    v = PhotoGallery(id)
    v.title = unicode(title, 'UTF-8')
    context._setObject(id, v)
    add_and_edit(context, id, REQUEST)
    return ''        
