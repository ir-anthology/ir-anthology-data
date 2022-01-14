from setuptools import setup, find_packages

setup(
    name='ir-anthology-data',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pylatexenc',
        'wget',
        'urllib3',
        'nameparser',
        'nltk'
    ],
    entry_points='''
        [console_scripts]
        ir-anthology-data=main.manager:main
    ''',
)