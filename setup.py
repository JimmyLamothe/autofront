import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'autofront',
    version = '0.1a3.dev8',
    author = 'Jean-Michel Laprise',
    author_email = 'jmichel.dev@gmail.com',
    description = 'Automatic front end for Python project',
    keywords = 'automatic frontend front-end web browser interface flask school',
    license = 'BSD',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/JimmyLamothe/autofront',
    #project_urls = 'https://github.com/JimmyLamothe/autofront',
    packages = setuptools.find_packages(),
    package_data = {
        '' : ['static/*','static/css/*','templates/*']
    },
    include_package_data = False,
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
