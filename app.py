from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import tempfile
import shutil
import os
import zipfile
from pathlib import Path

from download_car import DownloadCar, State, Polygon
from download_car.drivers import Tesseract

app = FastAPI()


def zip_shapefile(shp_path: str) -> str:
    base = os.path.splitext(shp_path)[0]
    exts = [".shp", ".shx", ".dbf", ".prj"]
    files = [base + ext for ext in exts if os.path.exists(base + ext)]
    zip_path = base + ".zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            zipf.write(f, arcname=os.path.basename(f))
    return zip_path


def extract_and_find_shp(upload_file: UploadFile, temp_dir: str) -> str:
    zip_path = os.path.join(temp_dir, upload_file.filename)
    with open(zip_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    shp_path = None
    for root, _dirs, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(".shp"):
                shp_path = os.path.join(root, file)
    if shp_path:
        return shp_path
    raise ValueError(f"No .shp file found in zip '{upload_file.filename}'.")


@app.post("/download_state")
async def download_state_endpoint(
    state: str = Form(...),
    polygon: str = Form(...),
    folder: str = Form(None),
    tries: int = Form(25),
    debug: bool = Form(False),
    timeout: int = Form(30),
    max_retries: int = Form(5),
):
    try:
        car = DownloadCar(driver=Tesseract)
        path = car.download_state(
            state=State[state.upper()],
            polygon=Polygon[polygon.upper()],
            folder=folder,
            tries=tries,
            debug=debug,
            timeout=timeout,
        )
        zip_path = zip_shapefile(str(path))
        zip_file_handle = open(zip_path, "rb")
        return StreamingResponse(
            zip_file_handle,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{state}_{polygon}.zip"'},
        )
    except Exception as exc:
        return {"error": str(exc)}


@app.post("/download_country")
async def download_country_endpoint(
    polygon: str = Form(...),
    folder: str = Form("brazil"),
    tries: int = Form(25),
    debug: bool = Form(False),
    timeout: int = Form(30),
):
    try:
        car = DownloadCar(driver=Tesseract)
        result = car.download_country(
            polygon=Polygon[polygon.upper()],
            folder=folder,
            tries=tries,
            debug=debug,
            timeout=timeout,
        )
        zip_paths = []
        for _state, path in result.items():
            zip_paths.append(zip_shapefile(str(path)))
        with tempfile.NamedTemporaryFile(delete=False) as zip_file:
            with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                for z in zip_paths:
                    zipf.write(z, os.path.basename(z))
            zip_file_path = zip_file.name
        zip_file_handle = open(zip_file_path, "rb")
        return StreamingResponse(
            zip_file_handle,
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="brazil_{polygon}.zip"'},
        )
    except Exception as exc:
        return {"error": str(exc)}
