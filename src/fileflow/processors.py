from dataclasses import replace
from .core import FileProcessor, FileData


class StripProcessor(FileProcessor):
    def process(self, file: FileData) -> FileData:
        lines = (line.strip() for line in file.content.splitlines())
        new_content = "\n".join(lines)
        return replace(file, content=new_content)


class LowercaseProcessor(FileProcessor):
    def process(self, file: FileData) -> FileData:
        return replace(file, content=file.content.lower())


class ReplaceProcessor(FileProcessor):
    def __init__(self, old: str, new: str) -> None:
        self.old = old
        self.new = new

    def process(self, file: FileData) -> FileData:
        return replace(file, content=file.content.replace(self.old, self.new))


class DropEmptyProcessor(FileProcessor):
    def process(self, file: FileData) -> FileData:
        lines = (line for line in file.content.splitlines() if line.strip() != "")
        new_content = "\n".join(lines)
        return replace(file, content=new_content)

class GrepProcessor(FileProcessor):
    def __init__(self, substr: str) -> None:
        self.substr = substr

    def process(self, file: FileData) -> FileData:
        lines = (line for line in file.content.splitlines() if self.substr in line)
        new_content = "\n".join(lines)
        return replace(file, content=new_content)

class HeadProcessor(FileProcessor):
    def __init__(self, n: int) -> None:
        self.n = n

    def process(self, file: FileData) -> FileData:
        if self.n <= 0:
            raise ValueError("n must be positive")

        lines = file.content.splitlines()
        new_content = "\n".join(lines[:self.n])
        return replace(file, content=new_content)

class TailProcessor(FileProcessor):
    def __init__(self, n: int) -> None:
        self.n = n

    def process(self, file: FileData) -> FileData:
        if self.n <= 0:
            raise ValueError("n must be positive")

        lines = file.content.splitlines()
        new_content = "\n".join(lines[-self.n:])
        return replace(file, content=new_content)

