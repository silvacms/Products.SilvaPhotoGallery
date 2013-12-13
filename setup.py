# Copyright (c) 2002-2008 Infrae. All rights reserved.
# See also LICENSE.txt

from setuptools import setup, find_packages
import os

version = '1.0dev'

def product_readme(filename):
    f = open(os.path.join('Products', 'SilvaPhotoGallery', filename))
    try:
        return f.read()
    finally:
        f.close()


setup(name='Products.SilvaPhotoGallery',
      version=version,
      description="(Deprecated) Photogallery code source for Silva CMS",
      long_description=product_readme("README.txt") + "\n" +
                       product_readme("HISTORY.txt"),

      classifiers=[
              "Framework :: Zope2",
              "Programming Language :: Python",
              "Topic :: Software Development :: Libraries :: Python Modules",
              ],
      keywords='silva photo gallery deprecated',
      author='Infrae',
      author_email='info@infrae.com',
      url='https://github.com/silvacms/Products.SilvaPhotoGallery',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Products.Silva',
        ],
      )
