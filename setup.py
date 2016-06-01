import setuptools


setuptools.setup(
    name="qche",
    description="Filesystem-persisted cache with a dead simple interface",
    version="0.0.1",
    author="Raphael B.",
    author_email="rbaron@rbaron.net",
    license="MIT",
    keywords="cache filesystem",
    url="http://github.com/rbaron/qche",
    packages=setuptools.find_packages(exclude=["tests", "examples"]),
    extras_require={
        "dev": [
            "mock==2.0.0",
            "nose==1.3.7",
        ],
    }
)
