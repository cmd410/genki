import setuptools


with open('README.md', 'r') as file:
    long_description = file.read()


requires = [
    'cffi==1.14.3',
    'gevent==20.9.0',
    'greenlet==0.4.17',
    'pycparser==2.20',
    'zope.event==4.5.0',
    'zope.interface==5.1.2',
]

setuptools.setup(
    name='genki',
    version='0.0.1',
    author='Crystal Melting Dot',
    author_email='stresspassing@gmail.com',
    description='Asynchronous HTTP requests with gevent.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requires,
    url='https://github.com/cmd410/genki',
    packages=['genki', 'genki.http', 'genki.http.request', 'genki.http.constants'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
)
