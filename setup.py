from package_settings import NAME, VERSION, PACKAGES, DESCRIPTION
from setuptools import setup

setup(
    name=NAME,
    version=VERSION,
    long_description=DESCRIPTION,
    author='Bloomsbury AI',
    author_email='contact@bloomsbury.ai',
    packages=PACKAGES,
    package_dir={'docqa': 'document-qa/docqa'},
    include_package_data=True,
    install_requires=['Cython==0.27.3',
                      'dataclasses==0.6',
                      'pytest==3.6.4'],
    package_data={
        '': ['*.*'],
    },
)
