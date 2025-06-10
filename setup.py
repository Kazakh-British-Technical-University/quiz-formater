from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quiz-converter",
    version="0.1.0",
    author="Author",
    author_email="author@example.com",
    description="A tool for converting quiz questions from CSV to LaTeX and PDF exam variants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kazakh-British-Technical-University/quiz-formater/tree/develop",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "pandas>=1.3.0",
        "jinja2>=3.0.0",
        "tectonic>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "quiz-converter=main:app",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/test.tex", "config.ini"],
    },
) 