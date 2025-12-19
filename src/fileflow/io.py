from pathlib import Path
from .core import FileData, FileType


class UnknownFileTypeError(ValueError):
    pass


class FileReader:
    def __init__(self, path: str | Path):  #  Пользователь передаёт путь (str | Path)
        self.path = Path(path)             #  Мы превращаем его в Path

    def __enter__(self) -> FileData:
        if not self.path.exists():                #  файл существует?
            raise FileNotFoundError(self.path)

        file_type = self._detect_type()           #  Определяем FileType

        with self.path.open(encoding="utf-8") as f:    #  Читаем текст
            content = f.read()

        return FileData(
            path=str(self.path),
            content=content,
            file_type=file_type,
        )

    def __exit__(self, exc_type, exc, tb) -> bool:
        # ничего не подавляем
        return False

    def _detect_type(self) -> FileType:
        suffix = self.path.suffix.lower()             #  Смотрим suffix

        mapping = {
            ".txt": FileType.TEXT,
            ".csv": FileType.CSV,
            ".json": FileType.JSON,
        }

        try:
            return mapping[suffix]
        except KeyError:
            raise UnknownFileTypeError(f"Unsupported file type: {suffix}")
