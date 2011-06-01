# Copyright (c) 2003-2006 ETH Zurich, ID-TIM. Written by Benno Luthiger. All rights reserved.
# See also LICENSE.txt
# Inspired by Marc's SilvaPhotoGallery Code Source (some code was copied from that product too).
# i18n-ed by Wim Boucquaert wim@infrae.com thanks to Wirtschaftsuniversität Wien
# for making the i18n-ing possible

import os

#Zope
from Globals import InitializeClass, package_home
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from zope.interface import implements
from OFS.Image import Image

#Silva
from Products.SilvaExternalSources.interfaces import IExternalSource
from Products.SilvaExternalSources.CodeSource import CodeSource
from Products.Silva import SilvaPermissions
from Products.Silva.helpers import add_and_edit

#Formulator
from Products.Formulator.Form import ZMIForm
from Products.Formulator.XMLToForm import XMLToForm

#scripts
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

    # we know existing objects were already initialized, but
    # they didn't have this attribute yet and we don't want
    # to write an upgrade script because we're lazy :)
    _is_initialized = True

    def __init__(self, id):
        CodeSource.inheritedAttribute('__init__')(self, id)
        self._script_id = 'view'
        self._data_encoding = 'UTF-8'
        self._description = self.__doc__
        self._is_initialized = False

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

    security.declarePublic('getCaption')
    def getCaption(self, caption):
        lenCaption = 42
        if len(caption) < lenCaption:
            return caption
        return caption[:lenCaption-3] + '...'

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

def photo_gallery_moved(object, event):
    if not object._is_initialized:
        object._set_form()
        object._set_views()
        object._is_initialized = True
