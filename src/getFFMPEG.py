import shutil
import requests
import os

from tqdm import tqdm


def getFFMPEG(sysUsed, downloadDir):
    ffmpegPath = shutil.which("ffmpeg")
    if ffmpegPath is None:
        print("ffmpeg not found. Downloading ffmpeg...")
        ffmpegPath = downloadAndExtractFfmpeg(downloadDir, sysUsed)
    else:
        print(f"ffmpeg found in System Path: {ffmpegPath}")
    return ffmpegPath


def downloadAndExtractFfmpeg(downloadDir, sysUsed):
    print("Downloading ffmpeg")
    extractFunc = extractFfmpegZip if sysUsed == "Windows" else extractFfmpegTar
    os.makedirs(downloadDir, exist_ok=True)
    archiveName = "ffmpeg.zip" if sysUsed == "Windows" else "ffmpeg.tar.xz"
    ffmpegArchivePath = os.path.join(downloadDir, archiveName)

    ffmpegUrl = (
        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        if sysUsed == "Windows"
        else "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
    )

    try:
        response = requests.get(ffmpegUrl, stream=True)
        response.raise_for_status()
        totalSizeInBytes = int(response.headers.get("content-length", 0))
        chunkSize = 1024 * 1024

        with (
            open(ffmpegArchivePath, "wb") as file,
            tqdm(
                total=totalSizeInBytes,
                unit="B",
                unit_scale=True,
                desc="Downloading ffmpeg",
            ) as progressBar,
        ):
            for data in response.iter_content(chunk_size=chunkSize):
                if data:
                    file.write(data)
                    progressBar.update(len(data))
    except requests.RequestException as e:
        print(f"Failed to download ffmpeg: {e}")
        raise

    extractFunc(ffmpegArchivePath, downloadDir)
    return (
        os.path.join(downloadDir, "ffmpeg.exe")
        if sysUsed == "Windows"
        else os.path.join(downloadDir, "ffmpeg")
    )


def extractFfmpegZip(ffmpegZipPath, downloadDir):
    import zipfile

    try:
        with zipfile.ZipFile(ffmpegZipPath, "r") as zipRef:
            zipRef.extractall(downloadDir)
        ffmpegSrc = os.path.join(
            downloadDir, "ffmpeg-master-latest-win64-gpl", "bin", "ffmpeg.exe"
        )
        ffmpegDst = os.path.join(downloadDir, "ffmpeg.exe")
        if not os.path.exists(ffmpegDst):
            os.rename(ffmpegSrc, ffmpegDst)
    except zipfile.BadZipFile as e:
        print(f"Failed to extract ZIP: {e}")
        raise
    finally:
        os.remove(ffmpegZipPath)
        shutil.rmtree(os.path.join(downloadDir, "ffmpeg-master-latest-win64-gpl"))


def extractFfmpegTar(ffmpegTarPath, downloadDir):
    import tarfile

    try:
        with tarfile.open(ffmpegTarPath, "r:xz") as tarRef:
            tarRef.extractall(downloadDir)
        for item in os.listdir(downloadDir):
            fullPath = os.path.join(downloadDir, item)
            if (
                os.path.isdir(fullPath)
                and item.startswith("ffmpeg-")
                and item.endswith("-static")
            ):
                ffmpegSrc = os.path.join(fullPath, "ffmpeg")
                ffmpegDst = os.path.join(downloadDir, "ffmpeg")
                if not os.path.exists(ffmpegDst):
                    os.rename(ffmpegSrc, ffmpegDst)
                shutil.rmtree(fullPath)
    except tarfile.TarError as e:
        print(f"Failed to extract TAR: {e}")
        raise
    finally:
        os.remove(ffmpegTarPath)
