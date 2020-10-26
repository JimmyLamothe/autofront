from setuptools import find_packages, setup
import autofront

autofront.utilities.clear_local_files() #To make sure we never include local dir

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name = 'autofront',
    version = '0.1.1a3',
    author = 'Jean-Michel Laprise',
    author_email = 'jmichel.dev@gmail.com',
    description = 'Automatic front end for Python project',
    keywords = 'automatic frontend front-end web browser interface flask school',
    license = 'BSD',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/JimmyLamothe/autofront',
    project_urls = {
        'Documentation': 'https://github.com/JimmyLamothe/autofront/wiki'
        },
    packages = find_packages(),
    include_package_data = True, #To include MANIFEST.in in bdist
    install_requires = ['flask'],
    python_requires = '>=3.6',
    classifiers = [
       'Development Status :: 3 - Alpha',
       'Intended Audience :: Developers',
       'Topic :: Software Development :: User Interfaces',
       'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
       'Topic :: Home Automation',
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: BSD License',
       'Operating System :: OS Independent',
       ]
)
