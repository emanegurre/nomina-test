"""Extract payroll data from Mercedes-Benz Vitoria PDF payrolls."""

from __future__ import annotations

import argparse
import logging
import os
import re
from pathlib import Path
from typing import List, Optional

import pandas as pd
import pdfplumber

logging.basicConfig(level=logging.INFO)

NUMBER_RE = re.compile(r"[\d\.]*,\d{2}")


def parse_number(value: str) -> Optional[float]:
    """Convert a Spanish-formatted number to float.

    Dashes or empty values return ``None``.
    """
    value = value.strip()
    if not value or value in {"—", "-"}:
        return None
    value = value.replace(".", "").replace(",", ".")
    try:
        return float(value)
    except ValueError:
        return None


LINE_RE = re.compile(
    r"^(?P<code>\d+)\s+"  # line code
    r"(?P<concept>.+?)\s+"  # concept description
    r"(?P<units>[\d\.]*,\d{2}|—|-)\s+"  # units
    r"(?P<base>[\d\.]*,\d{2}|—|-)\s+"  # base
    r"(?P<devengo>[\d\.]*,\d{2}|—|-)\s+"  # devengo
    r"(?P<deduccion>[\d\.]*,\d{2}|—|-)"  # deduccion
)


def parse_nomina(path_pdf: Path) -> pd.DataFrame:
    """Parse Mercedes-Benz payroll PDF into a DataFrame.

    Parameters
    ----------
    path_pdf:
        Path to the PDF file.

    Returns
    -------
    pandas.DataFrame
        Extracted payroll concepts.
    """
    records: List[dict[str, Optional[float] | str]] = []
    with pdfplumber.open(str(path_pdf)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                line = line.strip()
                match = LINE_RE.match(line)
                if match:
                    gd = match.groupdict()
                    records.append(
                        {
                            "concepto": gd["concept"].strip(),
                            "unidades": parse_number(gd["units"]),
                            "base": parse_number(gd["base"]),
                            "devengo": parse_number(gd["devengo"]),
                            "deduccion": parse_number(gd["deduccion"]),
                        }
                    )
    return pd.DataFrame(
        records,
        columns=["concepto", "unidades", "base", "devengo", "deduccion"],
    )


def detect_downloads() -> Path:
    """Return the user's Downloads folder, ensuring it exists."""
    if os.name == "nt":
        base = Path(os.environ.get("USERPROFILE", Path.home()))
    else:
        base = Path.home()
    downloads = base / "Downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    return downloads


def save_to_csv(df: pd.DataFrame, output: Path) -> None:
    """Save the DataFrame to CSV."""
    df.to_csv(output, index=False)
    logging.info("Saved CSV to %s", output)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Extract payroll PDF to CSV")
    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument("-o", "--output", type=Path, help="CSV output path")
    parser.add_argument(
        "-d", "--to-downloads", action="store_true", help="Save CSV to Downloads"
    )
    args = parser.parse_args()

    df = parse_nomina(args.pdf)

    if args.to_downloads:
        output = detect_downloads() / f"{args.pdf.stem}.csv"
        save_to_csv(df, output)
    elif args.output:
        save_to_csv(df, args.output)
    else:
        print(df)


if __name__ == "__main__":
    main()
