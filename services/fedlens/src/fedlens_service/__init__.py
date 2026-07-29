"""Federal Reserve communication analysis for the DRL foundation."""

from .citations import CitedComparison, PassageCitation, cited_compare, search_passages
from .corpus import (
    CorpusDocument,
    FedCorpus,
    SourceRegisterEntry,
    load_fed_corpus,
    write_checksums_into_manifest,
)
from .service import FedDocument, FedLensService, LanguageComparison

__all__ = [
    "CitedComparison",
    "CorpusDocument",
    "FedCorpus",
    "FedDocument",
    "FedLensService",
    "LanguageComparison",
    "PassageCitation",
    "SourceRegisterEntry",
    "cited_compare",
    "load_fed_corpus",
    "search_passages",
    "write_checksums_into_manifest",
]

__version__ = "0.3.0"
