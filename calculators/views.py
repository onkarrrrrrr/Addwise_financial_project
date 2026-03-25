from django.shortcuts import render
import math

# 1. SIP Calculator
def sip_calculator(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('investment', 0))
        rate = float(request.POST.get('rate', 0))
        years = int(request.POST.get('years', 0))

        i = (rate / 100) / 12
        n = years * 12
        if i > 0 and n > 0:
            fv = p * (((1 + i)**n - 1) / i) * (1 + i)
            total_invested = p * n
            context = {
                'fv': round(fv, 2), 
                'invested': round(total_invested, 2), 
                'wealth_gained': round(fv - total_invested, 2)
            }
    return render(request, 'calculators/sip.html', context)

# 2. Lumpsum Calculator
def lumpsum_calculator(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('investment', 0))
        rate = float(request.POST.get('rate', 0))
        years = int(request.POST.get('years', 0))
        
        fv = p * ((1 + (rate / 100)) ** years)
        context = {
            'fv': round(fv, 2), 
            'invested': p, 
            'wealth_gained': round(fv - p, 2)
        }
    return render(request, 'calculators/lumpsum.html', context)

# 3. Step-Up SIP Calculator (Corrected Monthly Compounding)
def step_up_sip(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('investment', 0))
        rate = float(request.POST.get('rate', 0))
        years = int(request.POST.get('years', 0))
        step_up = float(request.POST.get('step_up', 0)) / 100

        total_fv, total_invested = 0, 0
        current_p = p
        
        for year in range(1, years + 1):
            i = (rate / 100) / 12  
            n_months = 12
            
            # Future value of this year's 12 months SIP
            fv_year = current_p * (((1 + i)**n_months - 1) / i) * (1 + i)
            
            # Compound the accumulated amount for the remaining months
            remaining_months = (years - year) * 12
            fv_compounded = fv_year * ((1 + i) ** remaining_months)
            
            total_fv += fv_compounded
            total_invested += (current_p * 12)
            current_p *= (1 + step_up) # Increase SIP for next year

        context = {
            'fv': round(total_fv, 2), 
            'invested': round(total_invested, 2), 
            'wealth_gained': round(total_fv - total_invested, 2)
        }
    return render(request, 'calculators/step_up_sip.html', context)

# 4. Step-Up vs Normal SIP Comparison
def stepup_vs_normal_sip(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('investment', 0))
        rate = float(request.POST.get('rate', 0))
        years = int(request.POST.get('years', 0))
        step_up = float(request.POST.get('step_up', 0)) / 100

        # Normal SIP Math
        i = (rate / 100) / 12
        n = years * 12
        normal_fv = p * (((1 + i)**n - 1) / i) * (1 + i) if i > 0 else 0
        normal_invested = p * n

        # Step-Up SIP Math
        step_up_fv, step_up_invested = 0, 0
        current_p = p
        for year in range(1, years + 1):
            fv_year = current_p * (((1 + i)**12 - 1) / i) * (1 + i)
            step_up_fv += fv_year * ((1 + i) ** ((years - year) * 12))
            step_up_invested += (current_p * 12)
            current_p *= (1 + step_up)

        context = {
            'normal_fv': round(normal_fv, 2),
            'normal_invested': round(normal_invested, 2),
            'step_up_fv': round(step_up_fv, 2),
            'step_up_invested': round(step_up_invested, 2),
            'difference': round(step_up_fv - normal_fv, 2)
        }
    return render(request, 'calculators/stepup_vs_normal.html', context)

# 5. Cost of Delay SIP
def cost_of_delay(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('investment', 0))
        rate = float(request.POST.get('rate', 0))
        years = int(request.POST.get('years', 0))
        delay_years = int(request.POST.get('delay_years', 0))

        i = (rate / 100) / 12
        n_normal = years * 12
        n_delayed = (years - delay_years) * 12

        fv_normal = p * (((1 + i)**n_normal - 1) / i) * (1 + i) if (i > 0 and n_normal > 0) else 0
        fv_delayed = p * (((1 + i)**n_delayed - 1) / i) * (1 + i) if (i > 0 and n_delayed > 0) else 0

        context = {
            'fv_now': round(fv_normal, 2),
            'fv_delayed': round(fv_delayed, 2),
            'cost_of_delay': round(fv_normal - fv_delayed, 2)
        }
    return render(request, 'calculators/cost_of_delay.html', context)

# 6. SWP Calculator
def swp_calculator(request):
    context = {}
    if request.method == "POST":
        total_inv = float(request.POST.get('total_investment', 0))
        withdrawal = float(request.POST.get('withdrawal', 0))
        rate = float(request.POST.get('rate', 0)) / 100 / 12
        years = int(request.POST.get('years', 0))
        
        months = years * 12
        balance = total_inv
        for _ in range(months):
            interest = balance * rate
            balance = balance + interest - withdrawal
            if balance <= 0:
                balance = 0
                break
        
        context = {
            'final_balance': round(balance, 2), 
            'total_withdrawal': round(withdrawal * months, 2)
        }
    return render(request, 'calculators/swp.html', context)

# 7. EMI Calculator
def emi_calculator(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('loan_amount', 0))
        rate = float(request.POST.get('rate', 0)) / 12 / 100
        years = float(request.POST.get('years', 0))
        n = int(years * 12)

        if rate > 0 and n > 0:
            emi = p * rate * ((1 + rate)**n) / (((1 + rate)**n) - 1)
        else:
            emi = p / n if n > 0 else 0

        total_payment = emi * n
        context = {
            'emi': round(emi, 2), 
            'total_interest': round(total_payment - p, 2), 
            'total_payment': round(total_payment, 2)
        }
    return render(request, 'calculators/emi.html', context)

# 8. Inflation Calculator
def inflation_calculator(request):
    context = {}
    if request.method == "POST":
        amount = float(request.POST.get('amount', 0))
        inflation = float(request.POST.get('inflation', 0)) / 100
        years = int(request.POST.get('years', 0))

        future_cost = amount * ((1 + inflation) ** years)
        purchasing_power = amount / ((1 + inflation) ** years)
        
        context = {
            'future_cost': round(future_cost, 2), 
            'purchasing_power': round(purchasing_power, 2)
        }
    return render(request, 'calculators/inflation.html', context)

# 9. FD Calculator (Quarterly Compounding usually used in India)
def fd_calculator(request):
    context = {}
    if request.method == "POST":
        p = float(request.POST.get('investment', 0))
        rate = float(request.POST.get('rate', 0)) / 100
        years = float(request.POST.get('years', 0))
        compounding_freq = 4 

        maturity = p * ((1 + (rate / compounding_freq)) ** (compounding_freq * years))
        context = {
            'maturity_amount': round(maturity, 2), 
            'interest_earned': round(maturity - p, 2)
        }
    return render(request, 'calculators/fd.html', context)

# 10. CAGR Calculator
def cagr_calculator(request):
    context = {}
    if request.method == "POST":
        initial = float(request.POST.get('initial_value', 0))
        final = float(request.POST.get('final_value', 0))
        years = float(request.POST.get('years', 0))

        if initial > 0 and years > 0:
            cagr = ((final / initial) ** (1 / years)) - 1
            context = {'cagr_percentage': round(cagr * 100, 2)}
    return render(request, 'calculators/cagr.html', context)

# 11. Dream Goal Calculator (Reverse SIP)
def dream_goal_calculator(request):
    context = {}
    if request.method == "POST":
        goal_amount = float(request.POST.get('goal_amount', 0))
        rate = float(request.POST.get('rate', 0))
        years = int(request.POST.get('years', 0))

        i = (rate / 100) / 12
        n = years * 12
        if i > 0 and n > 0:
            monthly_sip = goal_amount / ((((1 + i)**n - 1) / i) * (1 + i))
            context = {'required_monthly_sip': round(monthly_sip, 2)}
    return render(request, 'calculators/dream_goal.html', context)

# 12. Net Worth Calculator
def net_worth_calculator(request):
    context = {}
    if request.method == "POST":
        assets = float(request.POST.get('total_assets', 0))
        liabilities = float(request.POST.get('total_liabilities', 0))
        context = {'net_worth': round(assets - liabilities, 2)}
    return render(request, 'calculators/net_worth.html', context)

# 13. Life Cover Calculator
def life_cover_calculator(request):
    context = {}
    if request.method == "POST":
        monthly_expenses = float(request.POST.get('monthly_expenses', 0))
        liabilities = float(request.POST.get('liabilities', 0))
        current_savings = float(request.POST.get('current_savings', 0))
        years_to_provide = int(request.POST.get('years', 20)) 

        required_cover = (monthly_expenses * 12 * years_to_provide) + liabilities - current_savings
        context = {'recommended_cover': round(max(0, required_cover), 2)}
    return render(request, 'calculators/life_cover.html', context)

# 14. Retirement Calculator (Corrected with Annuity Due)
def retirement_calculator(request):
    context = {}
    if request.method == "POST":
        current_age = int(request.POST.get('current_age', 0))
        retire_age = int(request.POST.get('retire_age', 0))
        life_expectancy = int(request.POST.get('life_expectancy', 80))
        monthly_expenses = float(request.POST.get('monthly_expenses', 0))
        inflation = float(request.POST.get('inflation', 0)) / 100
        return_rate = float(request.POST.get('return_rate', 0)) / 100

        years_to_retire = max(0, retire_age - current_age)
        years_in_retirement = max(0, life_expectancy - retire_age)

        # Future expenses at retirement
        future_monthly_expenses = monthly_expenses * ((1 + inflation) ** years_to_retire)
        
        # Real Rate of Return
        real_rate = ((1 + return_rate) / (1 + inflation)) - 1
        real_monthly_rate = real_rate / 12
        n = years_in_retirement * 12

        if real_monthly_rate > 0:
            # Present Value of Annuity Due
            corpus = future_monthly_expenses * (((1 - (1 + real_monthly_rate)**-n)) / real_monthly_rate) * (1 + real_monthly_rate)
        else:
            corpus = future_monthly_expenses * n

        context = {
            'monthly_expense_at_retirement': round(future_monthly_expenses, 2),
            'required_corpus': round(corpus, 2)
        }
    return render(request, 'calculators/retirement.html', context)

# 15. STP Calculator (Basic Mathematical Approximation)
def stp_calculator(request):
    context = {}
    if request.method == "POST":
        lumpsum = float(request.POST.get('lumpsum', 0))
        transfer_amount = float(request.POST.get('transfer_amount', 0))
        debt_rate = float(request.POST.get('debt_rate', 0)) / 100 / 12
        equity_rate = float(request.POST.get('equity_rate', 0)) / 100 / 12
        months = int(request.POST.get('months', 0))

        debt_balance = lumpsum
        equity_balance = 0

        for _ in range(months):
            if debt_balance >= transfer_amount:
                transfer = transfer_amount
            else:
                transfer = debt_balance
            
            # Debt phase
            debt_interest = debt_balance * debt_rate
            debt_balance = debt_balance + debt_interest - transfer
            
            # Equity phase
            equity_interest = equity_balance * equity_rate
            equity_balance = equity_balance + equity_interest + transfer

        context = {
            'final_debt_balance': round(max(0, debt_balance), 2),
            'final_equity_balance': round(equity_balance, 2),
            'total_value': round(max(0, debt_balance) + equity_balance, 2)
        }
    return render(request, 'calculators/stp.html', context)