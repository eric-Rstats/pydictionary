from distutils.core import setup

setup(
    name='dictionary',
    version='0.1',
    requires=['lxml', 'requests'],
    packages=['dictionary', 'dictionary.common', 'dictionary.cn_dict'],
    url='',
    license='MIT License',
    author='Christopher Lee',
    author_email='',
    description='Chinese dictionary.'
)
