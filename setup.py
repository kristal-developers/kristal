from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Programming Language :: Python',
    'Intended Audience :: Science/Research'
]

with open('README.rst') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='kristal',
    license='MIT',
    description=__doc__,
    long_description=LONG_DESCRIPTION,
    install_requires=['numpy'],
    author='Magdalena Krzuś, Konrad Jałowiecki',
    author_email='magdalena.krzus@gmail.com',
    packages=find_packages(exclude=['tests']),
    inlude_package_data=True)
