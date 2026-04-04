"""FASTA format parsing and formatting utilities."""


def parse_fasta(fasta_text: str) -> list[dict]:
    """Parse FASTA formatted text into list of {header, sequence} dicts."""
    entries = []
    current_header = None
    current_seq_parts: list[str] = []

    for line in fasta_text.strip().split("\n"):
        line = line.strip()
        if line.startswith(">"):
            if current_header is not None:
                entries.append({
                    "header": current_header,
                    "sequence": "".join(current_seq_parts),
                })
            current_header = line[1:].strip()
            current_seq_parts = []
        elif line:
            current_seq_parts.append(line)

    if current_header is not None:
        entries.append({
            "header": current_header,
            "sequence": "".join(current_seq_parts),
        })

    return entries


def format_fasta(header: str, sequence: str, line_width: int = 80) -> str:
    """Format a sequence as FASTA with wrapped lines."""
    lines = [f">{header}"]
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i : i + line_width])
    return "\n".join(lines)
