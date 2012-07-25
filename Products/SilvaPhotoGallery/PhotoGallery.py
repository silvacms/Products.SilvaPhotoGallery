# -*- coding: utf-8 -*-
# Copyright (c) 2003-2006 ETH Zurich, ID-TIM. Written by Benno Luthiger. All rights reserved.
# See also LICENSE.txt
# Inspired by Marc's SilvaPhotoGallery Code Source (some code was
# copied from that product too).  i18n-ed by Wim Boucquaert
# wim@infrae.com thanks to Wirtschaftsuniversität Wien for making the
# i18n-ing possible

import os

#Zope
from App.class_init import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate

#Silva
from Products.SilvaExternalSources.CodeSource import CodeSource
from Products.Silva import SilvaPermissions
from Products.Silva.helpers import add_and_edit

#Formulator
from Products.Formulator.Form import ZMIForm
from Products.Formulator.XMLToForm import XMLToForm

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from silva.core.interfaces import IImage
from silva.core import conf as silvaconf
from silva.fanstatic import need

_home = os.path.join(os.path.dirname(__file__), 'www')


class IPhotoGalleryResources(IDefaultBrowserLayer):
    silvaconf.resource('lightbox.css')
    silvaconf.resource('photo_gallery.css')
    silvaconf.resource('prototype.js')
    silvaconf.resource('effects.js')
    silvaconf.resource('lightbox.js')
    silvaconf.resource('gallery_helper_scripts.js')


class PhotoGallery(CodeSource):
    """A photo gallery to show thumbnails and the original pictures
    within a Silva document.
    """
    silvaconf.zmi_addable(True)
    silvaconf.factory('manage_addPhotoGalleryForm')
    silvaconf.factory('manage_addPhotoGallery')
    meta_type = 'Silva Photo Gallery Source'
    security = ClassSecurityInfo()

    _is_initialized = True

    def __init__(self, id):
        super(PhotoGallery, self).__init__(id)
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
        with open(os.path.join(_home, 'photo_gallery_form.form')) as form:
            XMLToForm(form.read(), self.parameters)

    def _set_views(self):
        with open(os.path.join(_home, 'photo_gallery_view.pt')) as template:
            self._setObject('view', ZopePageTemplate('view', template.read()))

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'includeResources')
    def includeResources(self):
        need(IPhotoGalleryResources)
        return u''

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'getPhotos')
    def getPhotos(self, model):
        """Returns a sorted list of photos found in the container.
        """
        return model.get_container().get_non_publishables(IImage)

    security.declarePublic('getCaption')
    def getCaption(self, caption):
        lenCaption = 42
        if len(caption) < lenCaption:
            return caption
        return caption[:lenCaption-3].rstrip() + '...'


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
