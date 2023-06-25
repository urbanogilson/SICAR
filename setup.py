from distutils.core import setup

setup(
    name="SICAR",
    version="0.6.0",
    author="Gilson Urbano",
    author_email="hello@gilsonurbano.com",
    packages=["SICAR", "SICAR.drivers", "SICAR.tests"],
    url="https://github.com/urbanogilson/SICAR",
    license="https://github.com/urbanogilson/SICAR/blob/main/LICENSE",
    description="SICAR - Tool designed for students, researchers, data scientists or anyone who would like to have access to SICAR files.",
    long_description=open("README.md").read(),
    install_requires=[
        "requests>=2.27.1",
        "urllib3>=1.26.15",
        "pytesseract==0.3.10",
        "opencv-python>=4.6.0.66",
        "numpy>=1.22.4",
        "tqdm>=4.65.0",
        "matplotlib>=3.7.1",
    ],
    extras_require={
        "PADDLE": ["paddlepaddle==2.5.0rc0", "paddleocr==2.6.1.3"],
    },
)
