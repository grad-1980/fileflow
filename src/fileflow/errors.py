class FileFlowError(Exception):
    """Base exception for the fileflow package."""


class ProcessorError(FileFlowError):
    """Raised when a processor fails during pipeline execution."""

    def __init__(self, processor_name: str, message: str = "Processor failed") -> None:
        self.processor_name = processor_name
        super().__init__(f"{message}: {processor_name}")
