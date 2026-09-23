import csv
import os
from pathlib import Path
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class CSVReader:
    """Utility class to parse CSV test data files."""

    @staticmethod
    def get_csv_rows_as_tuples(file_path, skip_header=True):
        """Reads CSV file and returns data as a list of tuples, perfect for @pytest.mark.parametrize."""
        resolved_path = Path(file_path).resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {resolved_path}")

        data = []
        with open(resolved_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            if skip_header:
                next(reader, None)
            for row in reader:
                # Strip spaces and skip empty rows or comments
                cleaned_row = [item.strip() for item in row]
                if cleaned_row and not cleaned_row[0].startswith("#"):
                    data.append(tuple(cleaned_row))

        logger.info(f"Loaded {len(data)} test records from CSV: {resolved_path.name}")
        return data

    @staticmethod
    def get_csv_rows_as_dicts(file_path):
        """Reads CSV file and returns data as a list of dictionaries keyed by header column names."""
        resolved_path = Path(file_path).resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {resolved_path}")

        data = []
        with open(resolved_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned_dict = {k.strip(): v.strip() for k, v in row.items() if k}
                data.append(cleaned_dict)

        logger.info(f"Loaded {len(data)} test dict records from CSV: {resolved_path.name}")
        return data
