"""
Indian PAN Card Validator — Part D.

PAN Format: 5 uppercase letters, 4 digits, 1 uppercase letter
Example: ABCDE1234F

The 4th character indicates taxpayer type:
  P → Individual
  C → Company
  H → Hindu Undivided Family (HUF)
  F → Firm
  A → Association of Persons (AOP)
  T → Trust
  B → Body of Individuals (BOI)
  L → Local Authority
  J → Artificial Juridical Person
  G → Government
"""


def get_taxpayer_type(fourth_char):
    """Return the taxpayer type based on the 4th character of PAN."""
    types = {
        "P": "Individual",
        "C": "Company",
        "H": "Hindu Undivided Family (HUF)",
        "F": "Firm / Partnership",
        "A": "Association of Persons (AOP)",
        "T": "Trust",
        "B": "Body of Individuals (BOI)",
        "L": "Local Authority",
        "J": "Artificial Juridical Person",
        "G": "Government Entity",
    }
    return types.get(fourth_char, "Unknown taxpayer type")


def validate_pan(pan):
    """
    Validate an Indian PAN card number.

    Rules:
        - Must be exactly 10 characters
        - Characters 1-5: uppercase letters (A-Z)
        - Characters 6-9: digits (0-9)
        - Character 10: uppercase letter (A-Z)
        - 4th character must be a valid taxpayer code

    Args:
        pan (str): The PAN number to validate.

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    valid_fourth_chars = set("PCHFATBLJG")

    # Check 1: Must be exactly 10 characters
    if len(pan) != 10:
        return False, f"Invalid length: {len(pan)} characters (must be exactly 10)."

    # Check 2: First 5 characters must be uppercase letters
    for i in range(5):
        if not pan[i].isalpha() or not pan[i].isupper():
            return False, (
                f"Position {i + 1} must be an uppercase letter. "
                f"Found: '{pan[i]}'."
            )

    # Check 3: Characters 6-9 must be digits
    for i in range(5, 9):
        if not pan[i].isdigit():
            return False, (
                f"Position {i + 1} must be a digit (0-9). "
                f"Found: '{pan[i]}'."
            )

    # Check 4: Last character must be an uppercase letter
    if not pan[9].isalpha() or not pan[9].isupper():
        return False, (
            f"Position 10 must be an uppercase letter. "
            f"Found: '{pan[9]}'."
        )

    # Check 5: 4th character must be a valid taxpayer type
    if pan[3] not in valid_fourth_chars:
        return False, (
            f"4th character '{pan[3]}' is not a valid taxpayer code. "
            f"Valid codes: {', '.join(sorted(valid_fourth_chars))}."
        )

    return True, "Valid PAN number."


def print_pan_result(pan):
    """Print validation result for a given PAN."""
    pan = pan.strip().upper()
    is_valid, message = validate_pan(pan)

    print(f"\n  PAN          : {pan}")
    print(f"  Status       : {'VALID' if is_valid else 'INVALID'}")
    print(f"  Details      : {message}")

    if is_valid:
        taxpayer = get_taxpayer_type(pan[3])
        print(f"  Taxpayer Type: {taxpayer}")


def main():
    """Entry point for PAN validator."""
    print("\n" + "=" * 45)
    print("     INDIAN PAN CARD VALIDATOR")
    print("=" * 45)

    # Run built-in test cases
    test_pans = [
        "ABCDE1234F",   # Valid individual
        "AABCP1234F",   # Valid individual
        "ABCDE123F",    # Too short
        "ABCDE1234",    # Last char not letter
        "abcde1234f",   # Lowercase (auto-corrected by .upper())
        "ABCX51234F",   # 4th char not valid taxpayer code
        "ABC1E1234F",   # 4th position is digit, not letter
        "ABCDE123456",  # Digits in wrong position
        "AABCG7107R",   # Valid Government entity
    ]

    print("\n--- Automated Test Cases ---")
    for pan in test_pans:
        print_pan_result(pan)

    # Interactive mode
    print("\n--- Try Your Own ---")
    while True:
        user_pan = input("\nEnter PAN to validate (or 'q' to quit): ").strip()
        if user_pan.lower() == "q":
            break
        print_pan_result(user_pan)


if __name__ == "__main__":
    main()
