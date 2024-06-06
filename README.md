# Daily Earnings Automation Script

This project involves a daily automation script designed to calculate the daily earnings for each product in the MongoDB database. The script connects to the Mercado Pago API to retrieve all payments received on the day of execution. It then accesses the database to find the products associated with each store. Since Mercado Pago only provides the amount of the received payment, and we need to determine how much we earned for each product, the script compares the payment amounts with the stored product prices to calculate the total earnings per product. Finally, it utilizes the Google Drive API to access each Excel file created per product and inserts the total earnings.

## Technologies Used

For the development of this project, AWS cloud services were utilized. Specifically, Lambdas were employed with cron jobs for daily execution due to their low costs and high scalability. SQS facilitated sending messages with all the stores to execute, ensuring each store runs on a separate instance of each Lambda. CloudWatch logs were utilized for logging purposes, while IAM roles were used for Lambda permissions. MongoDB was employed to securely store encrypted information for each store. Finally, deployment was done using Serverless.

## Workflow

1. The script connects to the Mercado Pago API to retrieve all payments received on the day of execution.
2. It accesses the MongoDB database to find the products associated with each store.
3. The script compares the payment amounts with the stored product prices to calculate the total earnings per product.
4. Using the Google Drive API, the script accesses each Excel file created per product and inserts the total earnings.

## Deployment

The project is deployed using Serverless, making it easy to manage and scale. The deployment process ensures seamless execution of the daily earnings automation script.
