import setuptools

pkg_name="theiapod"

setuptools.setup(
    name=pkg_name,
    version="0.1.0",
    author="Jeremy Magland",
    author_email="jmagland@flatironinstitute.org",
    description="Self-host gitpod-style workspaces for github repositories using theia",
    url="https://github.com/magland/theiapod",
    packages=setuptools.find_packages(),
    package_data={},
    install_requires=[
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)