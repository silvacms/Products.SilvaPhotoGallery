# Copyright (c) 2003 ETH ID-TIM. All rights reserved.
# See also LICENSE.txt

import os

from AccessControl import allow_module

from Products.SilvaExternalSources import ExternalSource

import Products.SilvaPhotoGallery.PhotoGallery

def initialize(context):
    context.registerClass(
        PhotoGallery.PhotoGallery,
        constructors = (PhotoGallery.manage_addPhotoGalleryForm,
                        PhotoGallery.manage_addPhotoGallery),
        icon = os.path.join(
                os.path.abspath(
                    os.path.dirname(ExternalSource.__file__)
                ),
                'www/codesource.png')
        )

allow_module('Products.SilvaPhotoGallery.i18n')
