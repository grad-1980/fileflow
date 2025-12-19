from __future__ import annotations
from dataclasses import dataclass, field
from .core import FileData, FileProcessor
from .errors import ProcessorError


@dataclass(frozen=True)
class RunReport:
    chars_before: int  # длина content до обработки
    chars_after: int  # длина content после всех процессоров
    changed: bool  # изменился ли контент (True/False)
    steps: list[str]  # список имён процессоров в порядке применения


@dataclass
class Pipeline:
    processors: list[FileProcessor] = field(default_factory=list)

    def add(self, processor: FileProcessor) -> Pipeline:
        """Флюент-интерфейс (fluent interface): можно цепочкой .add(...).add(...)"""
        self.processors.append(processor)
        return self

    def run(self, file: FileData) -> FileData:
        """Прогоняем файл через процессоры по цепочке."""
        result, _ = self.run_with_report(file)
        return result

    def run_with_report(self, file: FileData) -> tuple[FileData, RunReport]:
        current = file
        steps = []

        for processor in self.processors:
            try:
                current = processor.process(current)
            except ProcessorError:
                raise
            except Exception as e:
                raise ProcessorError(processor.__class__.__name__) from e
            steps.append(processor.__class__.__name__)

        changed = file.content != current.content
        report = RunReport(
            chars_before=len(file.content),
            chars_after=len(current.content),
            changed=changed,
            steps=steps,
        )
        return current, report
