from MigrationScheduling.utils import extract_file_idx


def test_extract_file_idx():
    assert extract_file_idx("file123", "file") == 123
    assert extract_file_idx("fileABC", "file") == -1
    assert extract_file_idx("migrations13.txt", "migrations") == 13
    assert extract_file_idx("migration.csv", "migrations") == -1
