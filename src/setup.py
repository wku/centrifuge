import os
import sys
from setuptools import setup


with_zmq = True
with_redis = True
with_mongodb = True
with_postgresql = True

filtered_args = []

for arg in sys.argv:
    if arg == '--without-zmq':
        with_zmq = False
    elif arg == '--without-redis':
        with_redis = False
    elif arg == '--without-mongodb':
        with_mongodb = False
    elif arg == '--without-postgresql':
        with_postgresql = False
    else:
        filtered_args.append(arg)

sys.argv = filtered_args


if sys.argv[-1] == 'test':
    status = os.system("python -m unittest discover -p 'test_*.py'")
    sys.exit(1 if status > 127 else status)


def full_split(path, result=None):
    """
    Split a path name into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return full_split(head, [tail] + result)


EXCLUDE_FROM_PACKAGES = ['centrifuge/bin']


def is_package(package_name):
    for pkg in EXCLUDE_FROM_PACKAGES:
        if package_name.startswith(pkg):
            return False
    return True


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, package_data = [], {}


root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
project_dir = 'centrifuge'


for dir_path, dir_names, file_names in os.walk(project_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dir_names[:] = [
        d for d in dir_names if not d.startswith('.') and d != '__pycache__'
    ]
    parts = full_split(dir_path)
    package_name = '/'.join(parts)
    if '__init__.py' in file_names and is_package(package_name):
        packages.append(package_name)
    elif file_names:
        relative_path = []
        while '/'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('/'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in file_names])


install_requires = [
    'six==1.3.0',
    'tornado==3.2',
    'sockjs-tornado==1.0.0',
    'jsonschema==2.3.0',
    'toro==0.5',
    'WTForms==1.0.4'
]


if with_zmq:
    install_requires.append('pyzmq==14.0.1')
if with_redis:
    install_requires.append('toredis-fork==0.1.2')
if with_mongodb:
    install_requires.append('motor==0.1.2')
if with_postgresql:
    install_requires.append('Momoko==1.0.0')


def long_description():
    return "Simple open-source platform for real-time message " \
           "broadcasting in web applications"


setup(
    name='centrifuge',
    version='0.4.3dev',
    description="Simple real-time messaging in web applications",
    long_description=long_description(),
    url='https://github.com/FZambia/centrifuge',
    download_url='https://github.com/FZambia/centrifuge',
    author="Alexandr Emelin",
    author_email='frvzmb@gmail.com',
    license='BSD',
    packages=packages,
    package_data=package_data,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'centrifuge = centrifuge.node:main',
            'xpub_xsub = centrifuge.proxy:main'
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ]
)
