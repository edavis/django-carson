from setuptools import setup, find_packages
import carson

setup(
    name         = "django-carson",
    version      = carson.__version__,
    packages     = find_packages(exclude=["example_project"]),
    url          = "https://github.com/edavis/django-carson",
    author       = "Eric Davis",
    author_email = "ed@npri.org",
)
