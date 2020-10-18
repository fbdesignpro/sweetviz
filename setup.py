import setuptools
from sweetviz import __title__, __version__, __author__, __license__

with open("README.md", "r") as fh:
    long_description_from_file = fh.read()

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email="fb@fbdesignpro.com",
    description="A pandas-based library to visualize and compare datasets.",
    long_description=long_description_from_file,
    long_description_content_type="text/markdown",
    url="https://github.com/fbdesignpro/sweetviz",
    packages=setuptools.find_packages(),
	license=__license__,
	include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Intended Audience :: Developers",
		"Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Topic :: Scientific/Engineering :: Visualization",
		"Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="pandas data-science data-analysis python eda",
    python_requires='>=3.6',
	install_requires=[
		'pandas>=0.25.3,!=1.0.0,!=1.0.1,!=1.0.2',
		'numpy>=1.16.0',
		'matplotlib>=3.1.3',
		'tqdm>=4.43.0',
		'scipy>=1.3.2',
		'jinja2>=2.11.1',
		'importlib_resources>=1.2.0'
		]
)
