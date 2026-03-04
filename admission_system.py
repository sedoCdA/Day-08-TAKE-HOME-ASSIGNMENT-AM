"""
University Admission Decision System.

Evaluates student eligibility based on academic and non-academic criteria.
Handles category-wise cutoffs, bonus rules, and scholarship decisions.
"""


def get_float_input(prompt, min_val, max_val):
    """Prompt user for a float and validate it within a range."""
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_choice_input(prompt, valid_choices):
    """Prompt user for a string and validate it against valid choices."""
    while True:
        value = input(prompt).strip().lower()
        if value in valid_choices:
            return value
        print(f"Enter one of: {', '.join(valid_choices)}")


def collect_inputs():
    """Collect and validate all student inputs."""
    print("\n" + "=" * 50)
    print("     UNIVERSITY ADMISSION SYSTEM")
    print("=" * 50)

    entrance_score = get_float_input("Entrance Score (0-100)      : ", 0, 100)
    gpa = get_float_input("GPA (0-10)                  : ", 0, 10)
    recommendation = get_choice_input("Recommendation (yes/no)     : ", ["yes", "no"])
    category = get_choice_input(
        "Category (general/obc/sc_st): ", ["general", "obc", "sc_st"]
    )
    extracurricular = get_float_input("Extracurricular Score (0-10) : ", 0, 10)

    return entrance_score, gpa, recommendation, category, extracurricular


def apply_bonus(entrance_score, recommendation, extracurricular):
    """Apply bonus points for recommendation and extracurricular score."""
    bonus = 0
    bonus_details = []

    if recommendation == "yes":
        bonus += 5
        bonus_details.append("+5 (recommendation)")

    if extracurricular > 8:
        bonus += 3
        bonus_details.append("+3 (extracurricular)")

    effective_score = entrance_score + bonus
    return effective_score, bonus, bonus_details


def get_category_cutoff(category):
    """Return the minimum entrance score required for a given category."""
    if category == "general":
        return 75
    elif category == "obc":
        return 65
    else:
        return 55  # sc_st


def evaluate_admission(entrance_score, gpa, recommendation, category, extracurricular):
    """
    Evaluate admission decision based on all criteria.

    Returns a tuple of (result, reason, effective_score, bonus_details).
    """
    # --- Merit Rule: Auto-admit with scholarship ---
    if entrance_score >= 95:
        return (
            "ADMITTED (Scholarship)",
            "Entrance score >= 95 — automatic scholarship admission.",
            entrance_score,
            [],
        )

    # --- Apply Bonus Points ---
    effective_score, bonus, bonus_details = apply_bonus(
        entrance_score, recommendation, extracurricular
    )

    # --- Get category cutoff ---
    cutoff = get_category_cutoff(category)
    category_display = category.upper().replace("_", "/")

    # --- Check GPA first ---
    if gpa < 7.0:
        return (
            "REJECTED",
            f"GPA {gpa} is below the minimum required GPA of 7.0.",
            effective_score,
            bonus_details,
        )

    # --- Check effective score against cutoff ---
    if effective_score >= cutoff:
        return (
            "ADMITTED (Regular)",
            (
                f"Meets {category_display} cutoff "
                f"({effective_score:.0f} >= {cutoff}) "
                f"and GPA requirement ({gpa} >= 7.0)."
            ),
            effective_score,
            bonus_details,
        )

    elif effective_score >= cutoff - 5:
        return (
            "⏳ WAITLISTED",
            (
                f"Effective score {effective_score:.0f} is close to "
                f"{category_display} cutoff of {cutoff} but did not meet it."
            ),
            effective_score,
            bonus_details,
        )

    else:
        return (
            "REJECTED",
            (
                f"Effective score {effective_score:.0f} is below "
                f"{category_display} cutoff of {cutoff}."
            ),
            effective_score,
            bonus_details,
        )


def print_result(
    entrance_score,
    effective_score,
    bonus_details,
    bonus,
    result,
    reason,
):
    """Print the formatted admission result."""
    print("\n" + "-" * 50)
    print("  ADMISSION RESULT")
    print("-" * 50)

    if bonus_details:
        print(f"  Bonus Applied   : {' '.join(bonus_details)}")
        print(f"  Original Score  : {entrance_score:.0f}")
        print(f"  Effective Score : {effective_score:.0f}")
    else:
        print(f"  Effective Score : {effective_score:.0f} (no bonus applied)")

    print(f"\n  Result  : {result}")
    print(f"  Reason  : {reason}")
    print("=" * 50 + "\n")


def main():
    """Entry point for the admission system."""
    entrance_score, gpa, recommendation, category, extracurricular = collect_inputs()

    result, reason, effective_score, bonus_details = evaluate_admission(
        entrance_score, gpa, recommendation, category, extracurricular
    )

    bonus = sum(
        [5 if recommendation == "yes" else 0, 3 if extracurricular > 8 else 0]
    )

    print_result(entrance_score, effective_score, bonus_details, bonus, result, reason)


if __name__ == "__main__":
    main()
