from setuptools import setup, find_packages
import carson

setup(
    name             = "django-carson",
    version          = carson.__version__,
    packages         = find_packages(exclude=["example_project"]),
    url              = "https://github.com/edavis/django-carson",
    author           = "Eric Davis",
    author_email     = "ed@npri.org",
    description      = "Easily store and display tweets from a set of users or tweets about a given topic",
    long_description = open('README.rst').read(),
    install_requires = [
        "pytz==2011h",
        "oauth2==1.5.170",
        "requests==0.6.1",
    ],
    classifiers      = [
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
    ],
)
