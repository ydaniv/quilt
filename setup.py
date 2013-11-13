from setuptools import setup


setup(
    name='fabulous',
    version='0.1',
    description='Fabulous is a simple set of Fabric tasks for use in small Django and Flask projects.',
    url='https://github.com/pwalsh/fabulous',
    author='Paul Walsh',
    author_email='paulywalsh@gmail.com',
    license='BSD',
    packages=['fabulous', 'fabulous.local', 'fabulous.remote', 'fabulous.contrib'],
    zip_safe=False,
)
