import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="gcs-uploader",
    version="0.0.1",
    author="Daniel Komesu",
    author_email="danielkomesu@gmail.com",
    description="Upload files to Google Cloud Storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=["google-cloud-storage"],
    packages=setuptools.find_packages(),
)
