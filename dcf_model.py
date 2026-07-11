"""
 DCF Valuation Model
=======================
A beginner Python project that estimates what a company is "worth"
based on projected future cash flows, discounted back to today's dollars.

WHAT IS A DCF:
A dollar you receive today is worth more than a dollar you receive in
X years. A DCF
values a company by:
  1. Projecting how much cash the company will generate in future years
  2. Discounting each future year's cash back to what it's worth
     today (using a discount rate)
  3. Adding up all those discounted values, plus a "terminal value"
     (an estimate of the company's worth beyond the projection window)
  4. Dividing by shares outstanding to get an estimated fair value
     PER SHARE, which you can then compare to the actual stock price

This is intentionally a simplified version of a real DCF (real ones
account for many more line items -- capex, working capital changes,
tax nuances, etc). This version is meant to demonstrate an understanding of the core mechanics.
Any company's information can manually be put in to this. 
"""


def project_cash_flows(starting_fcf, growth_rate, years):
    projected_flows = []
    current_fcf = starting_fcf

    for year in range(1, years + 1):
        current_fcf = current_fcf * (1 + growth_rate)
        projected_flows.append(current_fcf)
    return projected_flows
"""
this function takes today's cash flow and "rolls it forward" year by year,
 growing it by a fixed percentage each time, 
 and keeps a list of what it looked like at the end of each year.
"""

def discount_cash_flows(cash_flows, discount_rate):
    present_values = []

    for year, cash_flow in enumerate(cash_flows, start=1):
        present_value = cash_flow / (1 + discount_rate) ** year
        present_values.append(present_value)
    return present_values

"""
this function takes a list of future cash flows and converts every single one of them into 
"today's money",
 accounting for the fact that money later is worth less than money now.
"""

def calculate_terminal_value(final_year_fcf, discount_rate, terminal_growth_rate):
   next_year_fcf = final_year_fcf * (1 + terminal_growth_rate)
   terminal_value = next_year_fcf / (discount_rate - terminal_growth_rate)

   return terminal_value

"""
this function estimates "everything this company is worth beyond the years we explicitly projected,"
 by assuming it keeps generating slow, steady cash flow growth forever, 
 and folding all of that infinite future into one number.
"""

def calculate_dcf_valuation(starting_fcf, growth_rate, discount_rate, terminal_growth_rate, years, shares_outstanding):
    projected_flows= project_cash_flows(starting_fcf, growth_rate, years)

    present_values = discount_cash_flows(projected_flows, discount_rate)
    sum_of_present_values = sum(present_values)
    final_year_fcf = projected_flows[-1]
    terminal_value = calculate_terminal_value(final_year_fcf, discount_rate, terminal_growth_rate)
    discounted_terminal_value = terminal_value/(1+discount_rate)**years
    enterprise_value = sum_of_present_values + discounted_terminal_value
    fair_value_per_share = enterprise_value / shares_outstanding

    return {
        "projected_flows": projected_flows,
        "present_values": present_values,
        "sum_of_present_values": sum_of_present_values,
        "terminal_value": terminal_value,
        "discounted_terminal_value": discounted_terminal_value,
        "enterprise_value": enterprise_value,
        "fair_value_per_share": fair_value_per_share,
    }

"""
 this function calls the three earlier functions in the right order,
 combines their results, and calculates the two final numbers 
 (enterprise value and fair value per share) that everything else was building toward.
"""

def print_dcf_summary(dax_corp, valuation):
    print(f"-----DCF Valuation: {dax_corp}-----")
    print(f"Estimated Fair Value Per Share: ${valuation['fair_value_per_share']:.2f}")
    print(f"Total Estimated Enterprise Value: ${valuation['enterprise_value']:.2f}")
    print(f"Terminal Value(undiscounted): ${valuation['terminal_value']:.2f}")

    for year, flow in enumerate(valuation["projected_flows"], start=1):
        print(f" Year {year}: ${flow:,.2f}")

"""
This function makes the values come out in a presentable way 
instead of a list of roughly labeled numbers.
"""

def main():
    dax_corp = "Dax Corp"
    starting_fcf = 8700
    growth_rate = .09
    discount_rate = .1
    terminal_growth_rate = .03
    years = 5
    shares_outstanding = 1500

   
    valuation = calculate_dcf_valuation(starting_fcf, growth_rate, discount_rate, terminal_growth_rate, years, shares_outstanding)
    print_dcf_summary(dax_corp, valuation)
    
"""
This function sets the values of the variables based on the user's input"
"""
    
if __name__ == "__main__":
     main()




