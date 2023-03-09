from setuptools import setup

requires = [
    'avral',
    'fiona>=1.9.1',
    'shapely>=2.0.1',
]

setup(
    name='avral_crossing_borders',
    version='0.0.1',
    description='Calculate number of intersections of the geometry of objects with the geometries of borders',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='nextgis',
    author_email='info@nextgis.com',
    url='https://nextgis.com',
    keywords='',
    packages=['avral_crossing_borders'],

    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'avral_operations': [
            'avral_crossing_borders = avral_crossing_borders.operations:CrossingBorders',
        ],
    }
)
