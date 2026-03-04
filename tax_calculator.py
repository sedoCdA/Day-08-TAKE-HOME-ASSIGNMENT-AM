"""
Indian Income Tax Calculator — New Regime FY 2024-25.

Applies progressive slab-wise taxation with standard deduction.
Shows a full breakdown of tax per slab and effective tax rate.
"""


def get_income():
    """Collect and validate annual income from user."""
    while True:
        try:
            income = float(input("Enter Annual Income (₹): "))
            if income < 0:
                print("Income cannot be negative.")
            else:
                return income
        except ValueError:
            print("Please enter a valid number.")


def format_inr(amount):
    """Format a number in Indian Rupee lakhs/crores style."""
    amount = round(amount, 2)
    is_negative = amount < 0
    amount = abs(amount)
    rupees, paise = divmod(round(amount * 100), 100)
    rupees_str = str(rupees)

    if len(rupees_str) <= 3:
        formatted = rupees_str
    else:
        last_three = rupees_str[-3:]
        rest = rupees_str[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        formatted = ",".join(groups) + "," + last_three

    sign = "-" if is_negative else ""
    return f"₹{sign}{formatted}.{paise:02d}"


def calculate_tax(taxable_income):
    """
    Calculate progressive tax based on Indian New Regime slabs FY 2024-25.

    Slabs:
        0  – 3,00,000  →  0%
        3L – 7,00,000  →  5%
        7L – 10,00,000 → 10%
        10L – 12,00,000 → 15%
        12L – 15,00,000 → 20%
        Above 15,00,000 → 30%

    Returns a list of slab breakdowns and total tax.
    """
    slabs = [
        (300000, 0.00, "0 – 3,00,000"),
        (700000, 0.05, "3,00,001 – 7,00,000"),
        (1000000, 0.10, "7,00,001 – 10,00,000"),
        (1200000, 0.15, "10,00,001 – 12,00,000"),
        (1500000, 0.20, "12,00,001 – 15,00,000"),
        (float("inf"), 0.30, "Above 15,00,000"),
    ]

    breakdown = []
    total_tax = 0
    previous_limit = 0
    remaining = taxable_income

    for limit, rate, label in slabs:
        if remaining <= 0:
            break

        # How much of the income falls in this slab
        slab_size = min(limit - previous_limit, remaining)
        slab_tax = slab_size * rate

        breakdown.append(
            {
                "slab": label,
                "rate": rate * 100,
                "income_in_slab": slab_size,
                "tax": slab_tax,
            }
        )

        total_tax += slab_tax
        remaining -= slab_size
        previous_limit = limit

    return breakdown, total_tax


def print_tax_report(gross_income, standard_deduction, taxable_income, breakdown, total_tax):
    """Print the full tax breakdown report."""
    effective_rate = (total_tax / gross_income * 100) if gross_income > 0 else 0

    border = "═" * 58
    divider = "─" * 58

    print(f"\n{border}")
    print("        INCOME TAX CALCULATOR — NEW REGIME FY 2024-25")
    print(border)
    print(f"  Gross Annual Income    : {format_inr(gross_income):>18}")
    print(f"  Standard Deduction     : {format_inr(standard_deduction):>18}")
    print(f"  Taxable Income         : {format_inr(taxable_income):>18}")
    print(divider)
    print(f"  {'Slab':<28} {'Rate':>5}  {'Income':>12}  {'Tax':>10}")
    print(divider)

    for row in breakdown:
        if row["income_in_slab"] > 0:
            print(
                f"  {row['slab']:<28} "
                f"{row['rate']:>4.0f}%  "
                f"{format_inr(row['income_in_slab']):>12}  "
                f"{format_inr(row['tax']):>10}"
            )

    print(divider)
    print(f"  {'Total Tax Payable':<28}        {format_inr(total_tax):>22}")
    print(f"  {'Effective Tax Rate':<28}        {effective_rate:>21.2f}%")
    print(f"  {'Monthly Tax Deduction':<28}        {format_inr(total_tax / 12):>22}")
    print(f"{border}\n")

    # Tax saving tip
    if total_tax == 0:
        print("No tax payable — income is within the exempt slab.\n")
    elif effective_rate < 10:
        print(f"Your effective rate is low at {effective_rate:.1f}% — good tax position.\n")
    else:
        print(f"Effective rate: {effective_rate:.1f}% — consider tax-saving investments.\n")


def main():
    """Entry point for the tax calculator."""
    print("\n" + "═" * 58)
    print("        INDIAN INCOME TAX CALCULATOR")
    print("═" * 58)

    gross_income = get_income()
    standard_deduction = min(75000, gross_income)
    taxable_income = max(0, gross_income - standard_deduction)

    breakdown, total_tax = calculate_tax(taxable_income)
    print_tax_report(gross_income, standard_deduction, taxable_income, breakdown, total_tax)


if __name__ == "__main__":
    main()
