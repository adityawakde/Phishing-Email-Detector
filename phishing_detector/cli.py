"""
cli.py
------
Command-line interface for the phishing detector.

This is the ONLY file in the package that touches the console
(input/print). All actual detection logic lives in detector.py and is
imported here. This separation means Phase 2 (a Flask/FastAPI web
service) can import detector.py directly and never need this file.
"""

from phishing_detector.detector import analyze_email


def print_report(result: dict) -> None:
    """
    Print a formatted summary of the analysis to the console.

    Why a function: separating "computing the result" (detector.py)
    from "displaying the result" (here) means the display format can
    change freely without touching detection logic.

    Parameters:
        result (dict): Output of analyze_email().

    Returns:
        None
    """
    print("\n--- Phishing Detection Report ---")

    if result["keyword_hits"]:
        print("\nSuspicious phrases found:")
        for phrase, weight in result["keyword_hits"].items():
            print(f"  - '{phrase}' (weight: {weight})")
    else:
        print("\nNo suspicious phrases found.")

    if result["pattern_hits"]:
        print("\nSuspicious patterns found:")
        for pattern, weight in result["pattern_hits"].items():
            print(f"  - matched pattern: {pattern} (weight: {weight})")
    else:
        print("\nNo suspicious URL/pattern indicators found.")

    print(f"\nTotal Phishing Score: {result['score']}")
    print(f"Classification: {result['classification']}")
    print("----------------------------------\n")


def get_multiline_input() -> str:
    """
    Read multi-line email text from the user until a blank line.

    Why a function: isolating input-gathering from the main loop makes
    main() read top-to-bottom as a simple sequence of steps, and makes
    this easy to unit test by mocking input() in isolation.

    Returns:
        str: The full email text entered by the user.
    """
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    """
    Entry point: prompts the user for email text, runs the analysis,
    and prints the report.

    Why a function: keeping main() separate from analyze_email() means
    the detection logic can be imported and reused elsewhere (a web
    API in Phase 2, a batch scanner, a test suite) without triggering
    any input() calls.
    """
    print("=== Phishing Email Detector ===")
    print("Paste the email text below. Press Enter twice (blank line) when done:\n")

    email_text = get_multiline_input()

    if not email_text.strip():
        print("No text entered. Exiting.")
        return

    result = analyze_email(email_text)
    print_report(result)


if __name__ == "__main__":
    main()
