import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-vituvitu',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='A simple Django app to provide handy mixins and tools for daily development.',
    long_description=README,
    url='https://web.facebook.com/pierre.claver.banywerha',
    author='Pierre-Claver Koko Banywerha',
    author_email='pierreclaverkoko@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
