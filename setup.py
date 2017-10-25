from distutils.core import setup

setup(
    name='py_meteoblue',
    version='0.0.0',
    packages=['py_meteoblue', 'py_meteoblue.src'],
    package_dir={'py_meteoblue':
                     'py_meteoblue'},
    package_data={'py_meteoblue': ['py_meteoblue/config/*']},
    scripts=['scripts/purge_meteoblue.py'],
    url='',
    license='GPL v3',
    author='Tiago Ribeiro',
    author_email='tribeiro@ufs.br',
    description=''
)
