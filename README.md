# E-Wallet

This is a simple E-Wallet application that can be accessed via USSD interface. The application allows users to create an account, top up their wallet, make withdrawals, and request for balance and statements. The main notification channel for the application is via SMS.

## Table of Contents

- [Technologies](#Technologies)
- [Features](#Features)
- [Installation](#Installation)
- [Testing](#Testing)
- [interaction](#interaction)
- [License](#license)

## Technologies

The application is built using the following technologies:

- Python: Programming language used to build the application
- Flask: Web framework used to create the USSD application
- PostgreSQL: Relational database used to store user information and transaction details
- Redis: Used for efficient scheduling of tasks
- Africa's Talking API: Used for payment handling and SMS notifications to users

## Features

The application offers the following features:

- Account Creation: Users can create an account by entering their name and phone number.
- Top Up: Users can top up their wallet by entering the amount they wish to add.
- Withdraw: Users can withdraw money from their wallet by entering the amount they wish to withdraw.
- Check Balance: Users can check their wallet balance by selecting the balance option from the menu.
- Request Statement: Users can request for their transaction statement by selecting the statement option from the menu.

## Installation

To install and run the application, follow these steps:

1. Clone the repository to your local machine.
2. Install the Poetry dependency manager by following the instructions [here](https://python-poetry.org/docs/).
3. Install the dependencies using `poetry install`.
4. Create a PostgreSQL database and update the database URI in the `config.py` file.
5. Create an account with Africa's Talking and obtain your API key and username.
6. Update the Africa's Talking API credentials in the `config.py` file.
7. Start the application using `poetry run python app.py`.

## Testing

The application was developed using a test-driven approach, and tests are included in the `tests` folder. To run the tests, execute `poetry run flask test` from the command line.

## Continuous Integration/Continuous Deployment

The application is deployed to an AWS EC2 instance using a CI/CD pipeline with GitHub Actions. The pipeline automatically tests and deploys the application whenever code is pushed to the `main` branch. The configuration for the pipeline can be found in the `.github/workflows/deploy.yml` file.

## How It Works

### Account Creation

When a user dials the USSD code, they are prompted to create an account by entering their name and phone number.

![Account Creation](screenshots/create_account.gif)

### Top Up

Users can top up their wallet by entering the amount they wish to add.

![Top Up](screenshots/top_up.gif)

### Withdraw

Users can withdraw money from their wallet by entering the amount they wish to withdraw.

![Withdraw](screenshots/withdraw.gif)

### Check Balance

Users can check their wallet balance by selecting the balance option from the menu.

![Check Balance](screenshots/check_balance.gif)

### Request Statement

Users can request for their transaction statement by selecting the statement option from the menu.

![Request Statement](screenshots/request_statement.gif)

## Application Desing.

### Database Design
![database-design](design/db.png)
### User Registration Sequence
![register](design/register.png)
### Account Activation Sequence
![register](design/activate.png)

### Account Deactivation Sequence
![deactivate](design/deactivation.png)

### Account Topup Sequence
![register](design/topup.png)

### Account withdraw Sequence
![register](design/withdraw.png)

### Account Balance Request Sequence
![register](design/balance.png)

### Account Statement Request Sequence
![register](design/statement.png)

### User Initiated C2B Topup Sequence
![register](design/c2b.png)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
