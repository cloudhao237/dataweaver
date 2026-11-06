import os
import re
import csv
import json
from typing import List, Dict, Any, Optional

# Supported regex patterns
PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_intl": r"\+?[0-9]{1,3}?[-.\s]?\(?[0-9]{2,4}\)?[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}",
    "phone_cn": r"(?:(?:\+|00)86)?1[3-9]\d{9}",
    "url": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "id_card_cn": r"\b[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b"
}

class TextNormalizer:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Remove null bytes and non-printable chars (except whitespace)
        cleaned = "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")
        # Collapse multiple empty lines
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    @staticmethod
    def extract_entities(text: str, entity_types: Optional[List[str]] = None) -> Dict[str, List[str]]:
        if not entity_types:
            entity_types = list(PATTERNS.keys())
        
        results = {}
        for ent in entity_types:
            if ent in PATTERNS:
                matches = re.findall(PATTERNS[ent], text)
                # Deduplicate while preserving order
                seen = set()
                deduped = []
                for m in matches:
                    val = m.strip()
                    if val and val not in seen:
                        seen.add(val)
                        deduped.append(val)
                results[ent] = deduped
        return results

class BatchMerger:
    @staticmethod
    def merge_csv_files(file_paths: List[str], output_path: str, deduplicate: bool = True) -> Dict[str, Any]:
        """
        Merges multiple CSV/TSV files into one consolidated CSV file.
        Aligns headers automatically.
        """
        all_headers = []
        rows = []
        processed_files = 0
        total_records = 0

        for path in file_paths:
            if not os.path.exists(path):
                continue
            
            delimiter = "\t" if path.endswith(".tsv") else ","
            try:
                # Try UTF-8 first, fallback to gbk/latin-1
                encodings = ["utf-8-sig", "utf-8", "gb18030", "latin-1"]
                file_rows = None
                for enc in encodings:
                    try:
                        with open(path, "r", encoding=enc, errors="replace") as f:
                            reader = csv.DictReader(f, delimiter=delimiter)
                            if reader.fieldnames:
                                for h in reader.fieldnames:
                                    if h and h not in all_headers:
                                        all_headers.append(h)
                                file_rows = list(reader)
                                break
                    except Exception:
                        continue
                
                if file_rows:
                    rows.extend(file_rows)
                    processed_files += 1
            except Exception as e:
                print(f"Warning: Failed to process {path}: {e}")

        # Deduplication
        if deduplicate and rows:
            unique_rows = []
            seen_hashes = set()
            for r in rows:
                # Hash serialized row
                row_key = tuple(sorted(r.items()))
                if row_key not in seen_hashes:
                    seen_hashes.add(row_key)
                    unique_rows.append(r)
            rows = unique_rows

        total_records = len(rows)

        # Write consolidated output
        with open(output_path, "w", encoding="utf-8-sig", newline="") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=all_headers)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

        return {
            "processed_files": processed_files,
            "total_records": total_records,
            "columns": len(all_headers),
            "output_path": output_path
        }

    @staticmethod
    def extract_entities_to_csv(input_text_file: str, output_csv_path: str) -> Dict[str, Any]:
        """
        Reads raw text file and extracts structured entities (emails, phones, URLs) into CSV.
        """
        encodings = ["utf-8", "gb18030", "latin-1"]
        content = ""
        for enc in encodings:
            try:
                with open(input_text_file, "r", encoding=enc, errors="replace") as f:
                    content = f.read()
                    break
            except Exception:
                continue

        entities = TextNormalizer.extract_entities(content)
        
        # Format as rows
        max_len = max(len(v) for v in entities.values()) if entities else 0
        rows = []
        for i in range(max_len):
            row = {}
            for k, v in entities.items():
                row[k] = v[i] if i < len(v) else ""
            rows.append(row)

        headers = list(entities.keys())
        with open(output_csv_path, "w", encoding="utf-8-sig", newline="") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=headers)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

        return {
            "output_path": output_csv_path,
            "total_extracted": {k: len(v) for k, v in entities.items()}
        }
