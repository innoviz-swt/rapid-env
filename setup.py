import setuptools
from rapidenv import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='rapid-env',
    description="library with helpers for rapid development environment ramp up, build and distribution.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=setuptools.find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],


    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
            # If any package contains any file except .py include them as well:
            "": ["**/.*", "**/*.*"],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],

    # What does your project relate to?
    # keywords=[],

    # Choose your license
    license='MIT',

    python_requires='>=3.6',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': [],
    #     'test': [],
    # },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'renv=rapidenv.__main__:main',
            'mng=rapidenv.console_scripts:mng'
            # 'conan_server=conans.conan_server:run',
            # 'conan_build_info=conans.build_info.command:run'
        ],
    },
)
