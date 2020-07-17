import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='rapid-env',
    version='0.0.0',
	description="library with helpers for rapid development environment ramp up, build and distribution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],	
    python_requires='>=3.6',
	install_requires=[],
)