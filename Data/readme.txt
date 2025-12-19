Key Columns:

loan_id – Unique identifier; acts as the primary key of the dataset. 
address_state – State where the customer resides.
application_type – Type of loan application (Individual or Partnership).
emp_length – Number of years the customer has been working in their current company.    ✔️
emp_title – Position or job title of the customer in the organization.
grade – Grade level assigned to the loan.
home_ownership – Customer’s home ownership status (e.g., Rent, Mortgage, Own).          ✔️
issue_date – Date when the loan was issued.                                             ✔️
*Bonus* day_since_loan_was_issued                                                       
last_credit_pull_date – Most recent date when the customer’s credit history was checked.
last_payment_date – Date of the customer’s latest payment.                              
loan_status – Status of the loan (e.g., Fully Paid, Late, Default).                     💥 (MARK)
next_payment_date – Due date of the next EMI.
member_id – Unique ID of the customer.                                                  
purpose – Reason for taking the loan.                                                   ✔️
sub_grade – Sub-grade level of the loan.
term – Tenure or duration of the loan.                                                  ✔️
verification_status – Indicates whether the customer’s documents were verified.    
annual_income – Customer’s annual income.(Customer's monthly income)(income * +- 20 / 12)✔️                                         ️ 
dti – Debt-to-income ratio.                                                             
installment – Monthly EMI amount.
int_rate – Interest rate of the loan.                                                   ✔️!
loan_amount – Principal amount of the loan.                                             ✔️
total_acc – Total number of accounts held by the customer.                              ✔️
total_payment – Total amount received from the customer.                                
Domain Terminologies used in datasets :-

Month-to-Date :- Performance or total up to the current date in the current Month .
Formula :- MTD = Sum(Values from 1st of current month)
Example :- if everyday income is 2$ per day . and today is 8th November then MTD will be 16$.

Month-to-Month :- Change or growth from last month to this month.
Formula :- MTM = (Current Month Value – Previous Month Value ) / Previous Month Value * 100 %
Example:- If January Sales = 10k and Feb are 12k then MTM = (12-10k)/10k *100= 20%

Debt-to-Income :- Measures how much of your income goes toward paying debts.
Formula :- DTI = Total Month Debts Payments / Gross Income * 100%.
Example :- DTI=(30k/100k)*100 = 30 %