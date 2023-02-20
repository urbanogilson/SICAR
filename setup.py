from distutils.core import setup

setup(
    name="SICAR",
    version="0.4.2",
    author="Gilson Urbano",
    author_email="hello@gilsonurbano.com",
    packages=["SICAR", "SICAR.drivers", "SICAR.tests"],
    url="https://github.com/urbanogilson/SICAR",
    license="https://github.com/urbanogilson/SICAR/blob/main/LICENSE",
    description="SICAR - Tool designed for students, researchers, data scientists or anyone who would like to have access to SICAR files.",
    long_description=open("README.md").read(),
    install_requires=[
        "requests>=2.25.1",
        "urllib3>=1.24.3",
        "pytesseract==0.3.7",
        "opencv-python>=4.6.0",
        "numpy>=1.21.6",
        "tqdm>=4.64.1",
        "matplotlib>=3.2.2",
        "paddlepaddle==2.4.2",
        "paddleocr>=2.6.1",
    ],
)
