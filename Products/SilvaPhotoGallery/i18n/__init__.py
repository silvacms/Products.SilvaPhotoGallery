"""Provides a function called 'translate' that *must* be imported as '_':

    from Products.SilvaPhotoGallery.i18n import translate as _

and will provide a MessageFactory that returns Messages for
i18n'ing Product code and Python scripts.
"""
from zope.i18nmessageid import MessageFactory

translate = MessageFactory('silva_photo_gallery')
