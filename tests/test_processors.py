from fileflow import processors
from fileflow.core import FileData, FileType
from fileflow.pipeline import Pipeline


def test_drop_empty_processor():
    pipeline = Pipeline().add(processors.DropEmptyProcessor())
    file = FileData(
        path="x.txt",
        content="a\n\n   \nb\n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "a\nb"


def test_grep_processor():
    pipeline = Pipeline().add(processors.GrepProcessor("error"))
    file = FileData(
        path="x.txt",
        content="error\nok\nerror again\n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "error\nerror again"


def test_head_processor():
    pipeline = Pipeline().add(processors.HeadProcessor(2))
    file = FileData(
        path="x.txt",
        content="a\nb\nc\n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "a\nb"


def test_tail_processor():
    pipeline = Pipeline().add(processors.TailProcessor(2))
    file = FileData(
        path="x.txt",
        content="a\nb\nc\n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "b\nc"


def test_strip_processor():
    pipeline = Pipeline().add(processors.StripProcessor())
    file = FileData(
        path="x.txt",
        content="a  \nb\n  c   \n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "a\nb\nc"


def test_lowercase_processor():
    pipeline = Pipeline().add(processors.LowercaseProcessor())
    file = FileData(
        path="x.txt",
        content="A\nb\nC\n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "a\nb\nc\n"


def test_replace_processor():
    pipeline = Pipeline().add(processors.ReplaceProcessor(old="a", new="abc"))
    file = FileData(
        path="x.txt",
        content="a\nbbbb\ncbbba\n",
        file_type=FileType.TEXT,
    )

    result = pipeline.run(file)
    assert result.content == "abc\nbbbb\ncbbbabc\n"



