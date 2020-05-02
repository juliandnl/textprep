from setuptools import setup


def readme():
    with open('README.rst') as f:
        README = f.read()
    return README


setup(
    name="textprep",
    version="0.0.1",
    description="textprep - Text Preprocessing - NLP package for cleaning text",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    url="https://github.com/juliandnl/textprep",
    author="Julian Kortendieck",
    author_email="julian.kortendieck@gmail.com",
    license="MIT",
    keywords="text preprocessing, text cleaning, clean text, NLP, tidy text",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    packages=["textprep"],
    include_package_data=True,
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4'
    # install_requires=["collections"]

)
