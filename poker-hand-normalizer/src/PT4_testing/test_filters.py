from pathlib import Path
import pytest

from PT4_testing.helpers import (
    extract_ids_from_pt4_file,
    get_ids_from_parser,
    compare_id_lists,
)

FILTERS_DIR = Path(__file__).resolve().parent / "filters"


def available_filters():
    return [p.stem for p in FILTERS_DIR.glob("*.txt")]


@pytest.mark.parametrize("filter_name", available_filters())
def test_pt4_filter(filter_name):
    pt4_ids = extract_ids_from_pt4_file(f"{filter_name}.txt")
    parser_ids = get_ids_from_parser(filter_name)
    assert compare_id_lists(pt4_ids, parser_ids)
