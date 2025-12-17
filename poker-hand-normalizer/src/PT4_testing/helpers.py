from pathlib import Path
from handnormalizer.parser.pokerstars_stats_parser import HAND_ID_PATTERN
from handnormalizer.db.session import SessionLocal
from handnormalizer.db.models import Hand, PlayerHandStat

BASE_DIR = Path(__file__).resolve().parent
FILTERS_DIR = BASE_DIR / "filters"


def extract_ids_from_pt4_file(filename: str):
    path = FILTERS_DIR / filename
    text = path.read_text(encoding="utf-8")

    ids = []
    for line in text.splitlines():
        match = HAND_ID_PATTERN.search(line)
        if match:
            ids.append(match.group(1))
    return ids


def get_ids_from_parser(filter_name: str):
    session = SessionLocal()

    query = (
        session.query(Hand.site_hand_id)
        .join(PlayerHandStat)
        .filter(PlayerHandStat.player_name == Hand.hero_name)
    )

    if filter_name == "folded_flop_any":
        query = query.filter(PlayerHandStat.folded_flop_any.is_(True))
    elif filter_name == "bet_flop_any":
        query = query.filter(PlayerHandStat.bet_flop_any.is_(True))
    elif filter_name == "checked_flop":
        query = query.filter(PlayerHandStat.checked_flop.is_(True))
    else:
        raise ValueError(filter_name)

    rows = query.all()
    session.close()
    return [r[0] for r in rows]


def compare_id_lists(pt4_ids, parser_ids):
    pt4_set = set(pt4_ids)
    parser_set = set(parser_ids)

    missing_in_parser = pt4_set - parser_set
    extra_in_parser = parser_set - pt4_set

    if not missing_in_parser and not extra_in_parser:
        print("TODO OK! Exact match.")
        return True

    if missing_in_parser:
        print("IDs missing in parser (PT4 has them):", len(missing_in_parser))
        for x in sorted(missing_in_parser):
            print(x)

    if extra_in_parser:
        print("Extra IDs in parser (PT4 did not include them):", len(extra_in_parser))
        for x in sorted(extra_in_parser):
            print(x)

    return False
