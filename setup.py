import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streaminguploadserver",
    version="0.0.1",
    author="NteRySin",
    author_email="author@example.com",
    description="Streaming upload server in Python extended from http.server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NteRySin/streaminguploadserver",
    project_urls={
        "Bug Tracker": "https://github.com/NteRySin/streaminguploadserver/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'streaming_form_data @ git+https://github.com/NteRySin/streaming-form-data@patch-1#egg=streaming_form_data',
        'tqdm',
        'uploadserver @ git+https://github.com/Densaugeo/uploadserver#egg=uploadserver',
    ]
)
