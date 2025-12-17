from pathlib import Path

from handnormalizer import (
    PokerStarsStatsParser,
    SessionLocal,
    init_db,
    engine,
    clean_characters,
    remove_zoom,
    convert_euro_to_dollar_symbol,
    normalize_et_timestamp_to_us_format,
    anonymize_players,
)

def processor_pipeline(text: str) -> str:
    text = remove_zoom(text)
    text = convert_euro_to_dollar_symbol(text)
    text = normalize_et_timestamp_to_us_format(text)
    text = clean_characters(text)
    text, _ = anonymize_players(text)
    return text

def main():
    init_db(engine)

    parser = PokerStarsStatsParser(processor=processor_pipeline)
    session = SessionLocal()

    input_dir = Path("dataset")
    print("Files:", list(input_dir.glob("*.txt")))

    for file in input_dir.glob("*.txt"):
        print("Processing file:", file)
        raw_text = file.read_text(encoding="utf-8")
        hands = parser.split_hands(raw_text)

        for raw_hand in hands:
            try:
                hand, stats = parser.build_hand_and_stats(raw_hand)
                session.add(hand)
                for stat in stats:
                    session.add(stat)
            except Exception:
                continue

    session.commit()
    session.close()

if __name__ == "__main__":
    main()
