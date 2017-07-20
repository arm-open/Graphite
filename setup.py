from distutils.core import setup

setup(
  name = 'graphite-analytics',
  packages = ['graphite'],
  package_data={
    'graphite' : ['graphite.py', 'capture.js', 'templates/css/styles.css', 'templates/js/Chart.PieceLabel.js', 'templates/html/render.html', 'templates/fonts/Antro_Vectra.otf', 'templates/images/Calendar-icon.png'],
  },
  version = '0.1.2.16',
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