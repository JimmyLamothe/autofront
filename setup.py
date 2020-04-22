import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'autofront',
    version = '0.0.1a3',
    author = 'Jean-Michel Laprise',
    author_email = 'jmichel.dev@gmail.com',
    description = 'Automatic front end for Python project',
    keywords = 'automatic front end frontend web browser interface flask',
    license = 'BSD',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/JimmyLamothe/autofront',
    #project_urls = 'https://github.com/JimmyLamothe/autofront',
    packages = setuptools.find_packages(),
    include_package_data = True,
    install_requires = ['flask'],
    python_requires = '>=3',
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

