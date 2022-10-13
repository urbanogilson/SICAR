from distutils.core import setup

setup(
    name="SICAR",
    version="0.3.1",
    author="Gilson Urbano",
    author_email="gilson@gilsonurbano.com",
    packages=["SICAR", "SICAR.drivers", "SICAR.tests"],
    url="https://github.com/urbanogilson/SICAR",
    license="https://github.com/urbanogilson/SICAR/blob/main/LICENSE",
    description="SICAR - Tool designed for students, researchers, data scientists or anyone who would like to have access to SICAR files.",
    long_description=open("README.md").read(),
    install_requires=[
        "requests>=2.22.0",
        "urllib3>=1.24.3",
        "pytesseract==0.3.7",
        "opencv-python>=4.1.2.30",
        "numpy>=1.19.5",
        "tqdm>=4.56.2",
        "matplotlib>=3.2.2",
        "paddlepaddle==2.3.2",
        "paddleocr>=2.0.1",
    ],
)
