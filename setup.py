from distutils.core import setup
from glob import glob
import os

def find_dirs(dir_name):
    for dir, dirs, files in os.walk('.'):
        if dir_name in dirs:
            yield os.path.relpath(os.path.join(dir, dir_name))

# Find all of the man/info pages
data_files = []
man_sections = {}
for dir in find_dirs('man'):
    for file in os.listdir(dir):
        section = file.split('.')[-2]
        man_sections[section] = man_sections.get(section, []) + [os.path.join(dir, file)]
for section in man_sections:
    data_files.append(('share/man/man'+section, man_sections[section]))

setup(
  name = 'graphite-analytics',
  packages = ['graphite'],
  package_data={
    'graphite' : ['graphite.py', 'capture.js', 'templates/css/styles.css', 'templates/js/Chart.PieceLabel.js', 'templates/html/render.html', 'templates/fonts/Antro_Vectra.otf', 'templates/images/Calendar-icon.png'],
  },
  version = '0.1.2.17',
  description = 'Create a print-out template for your google analytics data',
  author = 'Arian Moslem',
  author_email = 'amoslem678@gmail.com',
  url = 'https://github.com/ARM-open/Graphite',
  include_package_data=True,
  zip_safe=True,
  classifiers = [],
  keywords = ['Google analytics', 'analytics', 'templates'], 
  install_requires=['Click', 'google-api-python-client', 'jinja2'],
  entry_points={'console_scripts': [
    'graphite-analytics = graphite.graphite:main'
  ]}
)