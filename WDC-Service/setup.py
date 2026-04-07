from setuptools import setup

setup(
    name='WDC-Service',
    version='1.0',
    packages=['wdc_service'],
    url='www.woodworkerswheelhouse.com',
    license='',
    author='Nayan Nath',
    author_email='nayanchandranath07@gmail.com',
    description='Web Service for Wood Delivery Calculator',
    install_requires=[
        "requests>=2.31.0",
        "Flask>=3.0.3",
        "Flask_Restful>=0.3.10",
        "Flask_HTTPAuth>=4.8.0"
    ],
    package_data={"wdc_service": ["delivery.db"]}
)
