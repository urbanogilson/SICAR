from distutils.core import setup

setup(
    name="SICAR",
    version="0.1.0",
    author="Gilson Urbano",
    author_email="gilson@gilsonurbano.com",
    packages=["SICAR"],
    scripts=["bin/sicar.py"],
    url="https://github.com/urbanogilson/SICAR",
    license="https://github.com/urbanogilson/SICAR/blob/main/LICENSE",
    description="SICAR - This tool is designed for students, researchers, data scientists or anyone who would like to have access to SICAR files.",
    long_description=open("README.md").read(),
    install_requires=[
        "requests==2.22.0",
        "urllib3==1.25.8",
        "pytesseract==0.3.7",
        "opencv-python==4.5.1.48",
        "numpy==1.19.5",
        "tqdm==4.56.2",
    ],
)