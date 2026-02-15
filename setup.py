from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="open-coscientist-agriculture",
    version="0.1.0",
    author="agroia-lab",
    author_email="",
    description="Multi-agent AI system for integrated weed management and precision farming research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agroia-lab/open-coscientist-agriculture",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.3.25",
        "langchain-community>=0.3.24",
        "langgraph>=0.4.7",
        "typing-extensions>=4.0.0",
        "ipython>=8.0.0",  # For notebook support
        "gpt-researcher @ git+https://github.com/assafelovic/gpt-researcher@v3.3.0",
        "langchain-core>=0.3.65",
        "langchain-community>=0.3.2",
        "langchain-openai>=0.3.18",
        "langchain-anthropic>=0.3.15",
        "langchain-google-genai>=2.1.5",
        "networkx>=3.5",
        "scikit-learn>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.23.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "ruff>=0.0.1",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
)
