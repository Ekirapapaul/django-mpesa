from setuptools import setup, find_packages

extras_require = {
    'test': [
        'cryptography',
    ],
    'lint': [
        'pep8',
    ],
    'dev': [
        'bumpversion>=0.5.3,<1',
        'wheel',
        'twine',
    ],
}

extras_require['dev'] = (
    extras_require['dev'] +
    extras_require['test'] +
    extras_require['lint']
)

setup(
    name='django-mpesa',
    version='2.0.13',
    description='A python library that interfaces safaricoms mpesa apis',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    url='https://www.vorane.com/',
    author='Paul Ekirapa',
    author_email='ekirapapaul@gmail.com',
    license='MIT',
    packages=find_packages(
        exclude=['tests', 'tests.*', 'licenses', 'requirements']),
    install_requires=[
        'Django>=2.2',
        'djangorestframework>=3.12.4',
        'requests>=2.22.0',
    ],
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]

)
