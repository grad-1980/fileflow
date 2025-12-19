from dataclasses import dataclass
from enum import Enum


class FileType(Enum):
    TEXT = "txt"
    CSV = "csv"
    JSON = "json"


@dataclass(frozen=True)
class FileData:
    path: str
    content: str
    file_type: FileType


class FileProcessor:
    def process(self, file: FileData) -> FileData:
        raise NotImplementedError
