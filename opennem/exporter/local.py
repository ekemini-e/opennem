import io
import logging
from io import BytesIO, StringIO
from os import makedirs
from pathlib import Path
from typing import Union

from opennem.settings import settings

logger = logging.getLogger(__name__)


def write_to_local(
    file_path: str, data: Union[StringIO, bytes, BytesIO, str]
) -> int:
    save_folder = settings.static_folder_path

    save_file_path = Path(save_folder) / file_path.lstrip("/")

    dir_path = save_file_path.resolve().parent

    if not dir_path.is_dir():
        makedirs(dir_path)

    if type(data) is io.StringIO:
        data = data.getvalue()

    bytes_written = 0

    with open(save_file_path, "w") as fh:
        bytes_written += fh.write(data)

    logger.info("Wrote {} to {}".format(bytes_written, save_file_path))

    return bytes_written
