from setuptools import setup


def readme():
    with open('README.md') as f:
        read = f.read()
    return read


setup(
    name="ADCT",
    version="1.1.2",
    description="A python package capable of performing and illustrating a few clustering methods.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/JJ8428/ADCT",
    author="Naga Venkata Sai Jagjit (JJ) Satti",
    author_email="nsatti.sc@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["ADCT"],
    include_package_data=True,
    install_requires=["numpy", "matplotlib"],
)
