from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='Quilt',
    version='0.2.0-alpha',
    description='(WIP) Quilt is an opinionated set of Fabric tasks for local '
                'development and remote deployment of web apps.',
    long_description=long_description,
    url='https://github.com/pwalsh/quilt',
    author='Paul Walsh',
    author_email='paulywalsh@gmail.com',
    license='BSD',
    packages=find_packages(),
    package_data={'': ['config.yaml']},
    install_requires=["Fabric >= 1.8.0", "PyYAML", "cuisine >= 0.6.5"],
    zip_safe=False,
)
