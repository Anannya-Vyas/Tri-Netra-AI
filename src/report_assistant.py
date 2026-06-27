"""
Tri-Netra — Report Assistant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generates a structured prompt template for a medical LLM to draft a brief,
3-sentence professional diagnostic note based on MRI analysis findings.

Author : Anannya Vyas
Email  : vyasanannya@gmail.com
GitHub : https://github.com/Anannya-Vyas/Tri-Netra-AI
"""

from __future__ import annotations


def generate_diagnostic_prompt(
    prediction_pct: float,
    tumor_type: str | None = None,
    timestamp: str | None = None,
) -> str:
    """Build an LLM prompt that requests a concise radiology-style diagnostic note.

    Parameters
    ----------
    prediction_pct : float
        Classification confidence as a percentage (0–100).
    tumor_type : str or None
        Tumor subtype identified by segmentation (e.g. "glioma",
        "meningioma", "pituitary").  Pass ``None`` or an empty string
        when segmentation was not performed or no tumor was detected.
    tumor_type : str or None
        Timestamp of the inference run (ISO-8601 or any human-readable
        format).  Included in the findings block so the note is traceable.

    Returns
    -------
    str
        A ready-to-send prompt string for any medical-capable LLM.
    """

    # ── Build the structured findings block ──────────────────────────
    tumor_label = tumor_type.strip() if tumor_type else "Not segmented / No tumor detected"
    ts_label = timestamp.strip() if timestamp else "N/A"

    confidence_descriptor = (
        "high" if prediction_pct >= 85
        else "moderate" if prediction_pct >= 50
        else "low"
    )

    findings_block = (
        f"  - Classification confidence : {prediction_pct:.1f}% ({confidence_descriptor})\n"
        f"  - Tumor type (segmentation) : {tumor_label}\n"
        f"  - Analysis timestamp        : {ts_label}"
    )

    # -- Assemble the full prompt -------------------------------------
    prompt = (
        "You are a board-certified neuroradiologist assistant AI.\n"
        "Based on the automated MRI analysis findings below, draft a\n"
        "professional diagnostic note for a radiologist's review.\n"
        "\n"
        "RULES:\n"
        "  1. Write exactly THREE concise sentences.\n"
        "  2. Sentence 1: State the primary finding (tumor presence/absence\n"
        "     and type, if available).\n"
        "  3. Sentence 2: Note the model's confidence level and any\n"
        "     clinical implication that warrants attention.\n"
        "  4. Sentence 3: Recommend a follow-up action (e.g. biopsy,\n"
        "     additional imaging, clinical correlation).\n"
        "  5. Use formal medical language appropriate for a radiology report.\n"
        "  6. Do NOT fabricate patient demographics or history.\n"
        "\n"
        "--- AUTOMATED FINDINGS ---------------------------\n"
        f"{findings_block}\n"
        "--------------------------------------------------\n"
        "\n"
        "Diagnostic Note:"
    )

    return prompt


# ── CLI demo ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample_prompt = generate_diagnostic_prompt(
        prediction_pct=92.4,
        tumor_type="Glioma (High-Grade)",
        timestamp="2026-06-26T23:30:00+05:30",
    )
    print("=" * 60)
    print("SAMPLE LLM PROMPT")
    print("=" * 60)
    print(sample_prompt)
    print("=" * 60)
