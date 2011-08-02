from setuptools import setup, find_packages

setup(
    name = "django-carson",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["pytz>=2011h", "oauth2==1.5.170"],
)
