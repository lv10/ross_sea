from setuptools import setup, find_packages

setup(
    name="RossSeaIce",
    version="0.0.1",
    description="Ross Sea Ice Analysis",
    url="https://rosssea.wordpress.com",
    author="lv10",
    author_email="luis@lv10.me",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7"
    ],
    packages=find_packages(exclude=["data"]),
    install_requires=[
        "argparse==1.2.1",
        "beautifulsoup4==4.4.1",
        "cycler==0.10.",
        "matplotlib==1.5.1",
        "numpy==1.11.0",
        "pandas==0.18.1",
        "pyparsing==2.1.4",
        "python-dateutil==2.5.3",
        "pytz==2016.4",
        "requests==2.10.0",
        "scipy==0.17.1",
        "six==1.10.0",
        "wsgiref==0.1.2",
    ],
)
