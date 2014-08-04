import os

os.environ['DJANGO_SETTINGS_MODULE'] = \
    'tests.settings'

from setuptools import setup

setup(
    name='djangocms_events',
    version='0.140804',
    author='http://www.aptivate.org/',
    author_email='support+djangocms_events@aptivate.org',
    packages=['djangocms_events'],
    include_package_data=True,
    url='https://github.com/aptivate/djangocms_events',
    license='LICENSE',
    description='Django-CMS events plugin and app',
    #long_description=open('README.md').read(),
    setup_requires = [ "setuptools_git >= 0.3", ],
    install_requires=[
        "Django", # 1.5 or 1.6
        "django-cms", # 2.4 or 3.0
        "south >= 0.8.4",
        "django-extended-choices >= 0.3.0",
        "django-appconf == 0.6",
    ],
    tests_require=[
    ],
    test_suite = "tests",
)
