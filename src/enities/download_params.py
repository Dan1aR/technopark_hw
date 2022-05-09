from dataclasses import dataclass, field
from typing import List


@dataclass()
class DownloadParams:
    paths: List[str]
    output_folder: str
    s3_bucket: str = field(default="for-dvc")
