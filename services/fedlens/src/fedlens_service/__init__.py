"""Federal Reserve communication analysis for the DRL foundation."""

from .corpus import (
    CorpusDocument,
    FedCorpus,
    SourceRegisterEntry,
    load_fed_corpus,
    write_checksums_into_manifest,
)
from .service import FedDocument, FedLensService, LanguageComparison

__all__ = [
    "CorpusDocument",
    "FedCorpus",
    "FedDocument",
    "FedLensService",
    "LanguageComparison",
    "SourceRegisterEntry",
    "load_fed_corpus",
    "write_checksums_into_manifest",
]

__version__ = "0.2.0"
