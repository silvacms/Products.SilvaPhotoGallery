# Copyright (c) 2003 ETH ID-TIM. All rights reserved.
# See also LICENSE.txt

from silva.core import conf as silvaconf

silvaconf.extension_name('SilvaPhotoGallery')
silvaconf.extension_title('Silva PhotoGallery')
silvaconf.extension_depends(["Silva", "SilvaExternalSources"])
silvaconf.extension_system()

