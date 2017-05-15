from setuptools import setup, find_packages

setup(
    name='dynamic_databases',
    version=__import__('dynamic_databases').__version__,
    description=(
        'Django App that allows for the addition of databases '
        'on the fly and also the ability to query the database'
        '\'s tables through dynamically generated models. '
    ),
    author='David Higgins',
    author_email='sligodave@gmail.com',
    url='https://github.com/sligodave/dynamic_databases/',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=[
        'django',
        'jsonfield'
    ],
    include_package_data=True,
    zip_safe=False,
)
