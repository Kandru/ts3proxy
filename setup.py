import sys
from setuptools import setup, find_packages

if sys.version_info < (3,):
    sys.stderr.write("Python < 3 is not supported\n")
    sys.exit(1)

install_requires = [
    "PyYAML",
]

setup(
    name="ts3proxy",
    version='0.3',
    author="Karl-Martin Minkner",
    author_email="support@kandru.de",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ts3proxy = ts3proxy.ts3proxy:main",
        ],
    },
)
