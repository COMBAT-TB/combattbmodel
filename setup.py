from setuptools import setup

setup(
    name='combat_tb_model',
    version='0.0.1',
    description='COMBAT-TB Graph Model,a Chado-derived graph model for genome annotation.',
    keywords='neo4j',
    packages=['combat_tb_model'],
    install_requires=[
        'py2neo'
    ]
)
