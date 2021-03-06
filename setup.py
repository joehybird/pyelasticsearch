# coding=utf-8

import codecs
import re
import sys

from os.path import join, dirname

# Prevent spurious errors during `python setup.py test`, a la
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html:
try:
    import multiprocessing
except ImportError:
    pass

from setuptools import setup, find_packages


PY2 = (sys.version_info < (3,0))


def read(filename):
    return codecs.open(join(dirname(__file__), filename), 'r').read()


def until_toc(text):
    """Return the part of ``text`` that comes before the "Contents" heading."""
    contents_position = text.index('\nContents\n')
    return text[:contents_position]


def replace_links(text):
    """Fix Sphinx links so rst2html doesn't choke on them on the PyPI page."""
    return (text
        .replace(':doc:`elasticsearch-py`',
                 u'`Comparison with elasticsearch-py, the “Official Client” <https://pyelasticsearch.readthedocs.org/en/latest/elasticsearch-py/>`_')
        .replace(':doc:`api`',
                 '`API Documentation <https://pyelasticsearch.readthedocs.org/en/latest/api/>`_')
        .replace(':func:`~pyelasticsearch.bulk_chunks()`',
                 '`bulk_chunks() <https://pyelasticsearch.readthedocs.org/en/latest/api/#pyelasticsearch.bulk_chunks>`_')
        .replace(':meth:`~pyelasticsearch.ElasticSearch.bulk()`',
                 '`bulk() <https://pyelasticsearch.readthedocs.org/en/latest/api/#pyelasticsearch.ElasticSearch.bulk>`_'))


def find_version(file_path):
    version_file = read(file_path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def install_requirements(file_path):
    with open(file_path, 'r') as reqs:
        return [line for line in (l.strip() for l in reqs) if line]


setup(
    name='pyelasticsearch',
    version=find_version(join('pyelasticsearch', '__init__.py')),
    description='Flexible, high-scale API to elasticsearch',
    long_description=(
        until_toc(replace_links(read('docs/source/index.rst')))
        + '\n\n'
        + '\n'.join(read(join('docs', 'source', 'changelog.rst')).splitlines()[1:])),
    author='Robert Eanes',
    author_email='python@robsinbox.com',
    maintainer='Erik Rose',
    maintainer_email='erik@mozilla.com',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # simplejson doesn't support 3.1 or 3.2.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
    ],
    install_requires=install_requirements('requirements.txt'),
    tests_require=['mock'] if PY2 else [],
    test_suite='pyelasticsearch.tests',
    url='https://github.com/pyelasticsearch/pyelasticsearch'
)
