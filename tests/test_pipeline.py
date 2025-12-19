import pytest

from fileflow.core import FileProcessor, FileData, FileType
from fileflow.errors import ProcessorError
from fileflow.pipeline import Pipeline


def test_pipeline_wraps_processor_error():
    class BrokenProcessor(FileProcessor):
        def process(self, file: FileData):
            raise ValueError("boom")

    pipeline = Pipeline().add(BrokenProcessor())
    file = FileData(
        path="x.txt",
        content="A\nb\nC\n",
        file_type=FileType.TEXT,
    )

    with pytest.raises(ProcessorError) as exc:
        pipeline.run(file)

    assert isinstance(exc.value.__cause__, ValueError)
