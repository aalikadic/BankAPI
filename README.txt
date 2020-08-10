This RestAPI was designed and developed to satisfy several technical as well as business requirements. It was developed using Python FastAPI
Framework together with MySQL as relational database. It was designed to be intuitive and easy to use. The documentation can be found online 
by visiting the API URL/docs. 

The application was designed to be easily buildable on other computers and self-contained. By using the requirements.txt and database
dump folder, recreating the environment and databaase shouldn't take up a lot of time.

The application satisfies the following business requirements:
• Create a customer with full name, day of birth, address and a rating class which defaults to
‚2‘.
• Query names and addresses of all customers by their last name and allow to sort the result.
• Transfer money from one account to another resulting in a posting.
• Create a new account for a given customer.
• Create a new credit for a given customer.
• List all accounts of one customer with their current balance.
• List all credits of one customer with their original term, remaining term, original credit
amount and the current credit amount.
• List all postings of the financial institution for a given booking date.
• List all postings with the account id and customer name of source and destination of one
customer and make the result sortable and page-able.
• Payoff a part of a credit by transferring money from an account
• Show the balance for one customer.
• Show the balance for the financial institution.
• The API should have an online documentation.
• List all credits with original credit amount, current credit amount and customer name which
are exceeded their original terms.
• If a customer paid off a credit, he will be awarded to a better rating class but at maximum to
‚1‘.
• If a customer did not pay off a credit before the remaining term is below zero his rating class
will be set to ‚4‘.
• List all customers with name grouped by their current rating class.

Adding authentication and authorization from this point on is fairly easy and the database has been set up in such a manner that
expanding and improving the application is rather easy.