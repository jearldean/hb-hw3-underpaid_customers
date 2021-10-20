import glob, os

# Well, this is just crying out for function-ization.
melon_cost = 1.00

# I think if a vendor came to me asking for a quarter, I wouldn't be buying many more
# melons from this petty scrooge. So, you can set that minimum ammount here.
# That's just good customer service.
# Set it to zero if you want, Ebenezer!
dont_pester_customers_owing_less_than = 0.5

def format_currency(a_nasty_float):
    rounded_float = round(a_nasty_float, 2)
    truncated_float = '%.2f' % rounded_float
    return f"${truncated_float}"

os.chdir(".")
# Could make more reports if * wildcard was used to identify files
for each_file in glob.glob("customer-orders.txt"):

    # Create lists to hold each 'column' of data
    customer_id = []
    customer = []
    quantity = []
    paid = []
    amount_owed = []

    the_file = open(each_file)
    for line in the_file:
        line = line.rstrip()  # Chop trailing whitespace
        words = line.split('|')  # Pipe is our data separation character

        customer_id.append(words[0])
        customer.append(words[1])
        quantity.append(words[2])
        paid.append(words[3])
        amount_owed.append((melon_cost * int(words[2])) - float(words[3]))
    
    the_file.close()  # Good practice to close the files you use.

    costumer_underpays = 0
    costumer_overpays = 0
    profits_shrinkage = 0.00
    refunds_to_issue = 0.00
    for ii in range(len(customer)):
        raw_money_owed = amount_owed[ii]
        if raw_money_owed > dont_pester_customers_owing_less_than:
            profits_shrinkage += raw_money_owed
            costumer_underpays += 1
            print(f"Customer Number {customer_id[ii]}:\t{customer[ii]} owes us {format_currency(raw_money_owed)}")
        elif amount_owed[ii] < 0:
            costumer_overpays += 1
            overpay = abs(raw_money_owed)
            refunds_to_issue += overpay
            print(f"Customer Number {customer_id[ii]}:\tWE OWE {customer[ii]} a {format_currency(overpay)} refund!")
    print(f"\n{costumer_underpays} customers owe us a total of {format_currency(profits_shrinkage)}")
    if costumer_overpays:
        customer_plural = "s" if costumer_overpays != 1 else ""
        print(f"WE OWE {costumer_overpays} customer{customer_plural} refunds totaling {format_currency(refunds_to_issue)}")
