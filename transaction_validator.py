"""
Smart Transaction Validator — Part E Bonus.

Rule-based fraud detection system for a fintech startup.
Supports VIP mode with doubled limits and ternary operator for dynamic limits.
"""


def get_float_input(prompt, min_val, max_val):
    """Collect and validate a float input."""
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"  Enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  Please enter a valid number.")


def get_choice_input(prompt, valid_choices):
    """Collect and validate a string choice."""
    while True:
        value = input(prompt).strip().lower()
        if value in valid_choices:
            return value
        print(f" Enter one of: {', '.join(valid_choices)}")


def collect_inputs():
    """Collect all transaction details from the user."""
    print("\n" + "=" * 50)
    print("     SMART TRANSACTION VALIDATOR")
    print("=" * 50)

    amount = get_float_input("Transaction Amount (₹)                  : ", 0.01, 10_000_000)
    category = get_choice_input(
        "Category (food/travel/electronics/other) : ",
        ["food", "travel", "electronics", "other"],
    )
    hour = int(get_float_input("Hour of Transaction (0-23)              : ", 0, 23))
    daily_spent = get_float_input("Amount Already Spent Today (₹)          : ", 0, 10_000_000)
    vip = get_choice_input("VIP Customer? (yes/no)                  : ", ["yes", "no"])

    return amount, category, hour, daily_spent, vip == "yes"


def validate_transaction(amount, category, hour, daily_spent, is_vip):
    """
    Validate a transaction against fraud detection rules.

    VIP customers get doubled limits on all thresholds.

    Args:
        amount (float): Transaction amount in rupees.
        category (str): Spending category.
        hour (int): Hour of transaction (0-23).
        daily_spent (float): Amount already spent today.
        is_vip (bool): Whether customer is VIP.

    Returns:
        tuple: (status, reason)
    """
    # Ternary operator to set limits dynamically based on VIP status
    single_limit = 100_000 if is_vip else 50_000
    daily_limit = 200_000 if is_vip else 100_000
    food_limit = 10_000 if is_vip else 5_000
    electronics_limit = 60_000 if is_vip else 30_000

    # --- BLOCK rules — these override everything ---
    if amount > single_limit:
        return (
            "BLOCKED",
            f"Exceeds single transaction limit of ₹{single_limit:,.0f}.",
        )

    if daily_spent + amount > daily_limit:
        return (
            "BLOCKED",
            (
                f"Daily limit of ₹{daily_limit:,.0f} would be exceeded. "
                f"(Already spent: ₹{daily_spent:,.0f} + ₹{amount:,.0f} = "
                f"₹{daily_spent + amount:,.0f})"
            ),
        )

    # --- FLAG rules ---
    if hour < 6 or hour > 23:
        return (
            "FLAGGED",
            f"Unusual transaction hour: {hour:02d}:00 (outside 06:00–23:00).",
        )

    # --- Category-specific limits ---
    if category == "food" and amount > food_limit:
        return (
            "FLAGGED",
            f"Food transaction ₹{amount:,.0f} exceeds category limit of ₹{food_limit:,.0f}.",
        )

    elif category == "electronics" and amount > electronics_limit:
        return (
            "FLAGGED",
            f"Electronics transaction ₹{amount:,.0f} exceeds category limit of ₹{electronics_limit:,.0f}.",
        )

    # --- All checks passed ---
    return "APPROVED", "Transaction meets all validation rules."


def print_transaction_result(amount, category, hour, daily_spent, is_vip, status, reason):
    """Print formatted transaction validation result."""
    print("\n" + "-" * 50)
    print("  TRANSACTION DETAILS")
    print("-" * 50)
    print(f"  Amount      : ₹{amount:,.2f}")
    print(f"  Category    : {category.capitalize()}")
    print(f"  Time        : {hour:02d}:00")
    print(f"  Daily Spent : ₹{daily_spent:,.2f}")
    print(f"  VIP Status  : {'Yes ' if is_vip else 'No'}")
    print("-" * 50)
    print(f"  Status      : {status}")
    print(f"  Reason      : {reason}")
    print("=" * 50 + "\n")


def main():
    """Entry point for transaction validator."""
    amount, category, hour, daily_spent, is_vip = collect_inputs()
    status, reason = validate_transaction(amount, category, hour, daily_spent, is_vip)
    print_transaction_result(amount, category, hour, daily_spent, is_vip, status, reason)


if __name__ == "__main__":
    main()
