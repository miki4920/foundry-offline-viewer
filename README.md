# Party Equipment Analyzer

## Description
The Party Equipment Analyzer is a Python Flask-based web application designed to display and analyze your party's equipment uploaded via the FoundryVTT Equipment Uploader. This application provides visualizations in both graph and table formats, allowing for comparisons of individual party members' wealth. This application is intended to be self-hosted and is Docker-compatible.

## Features
- **Visualization**: Display your party's equipment in clear, easy-to-understand graphs and tables.
- **Comparison**: Compare the wealth of individual party members based on their equipment.
- **Integration**: Seamlessly works with equipment data uploaded through the FoundryVTT Equipment Uploader.
- **Docker-compatible**: Easy to set up and run using Docker.

## Requirements
- Python 3.7 or higher
- Docker
- FoundryVTT Equipment Uploader data in a DynamoDB database
- AWS SDK installed on the server
- Flask
- Gunicorn

## Installation

### With Docker
1. Clone this repository: `git clone https://github.com/miki4920/party-equipment-analyzer.git`
2. Navigate to the cloned repository: `cd party-equipment-analyzer`
3. Build the Docker image: `docker build -t party-equipment-analyzer .`
4. Run the Docker container: `docker run -p 8000:8000 party-equipment-analyzer`

### Without Docker
1. Clone this repository: `git clone https://github.com/miki4920/party-equipment-analyzer.git`
2. Navigate to the cloned repository: `cd party-equipment-analyzer`
3. Install the requirements: `pipenv install`
4. Run the application: `gunicorn -w 4 app:app`

## Configuration
1. Set the necessary environment variables for your AWS credentials (Access Key ID, Secret Access Key) and DynamoDB table name. You can either add these to your environment or create a `.env` file in the root directory with the following entries:
    ```
    AWS_ACCESS_KEY_ID=youraccesskeyid
    AWS_SECRET_ACCESS_KEY=yoursecretaccesskey
    DYNAMODB_TABLE=yourtablename
    ```
2. If you are not using Docker, you may need to adjust the host and port in the `app.run()` command in `app.py`.

Please note: Never share your AWS credentials with anyone. Follow AWS security best practices. It is strongly recommended to use IAM roles with restricted permissions for this application.

## Usage
1. Once the application is running, navigate to `localhost:8000` (or your specified host and port) in your web browser.
2. You will be presented with a dashboard displaying the party's equipment in both graph and table formats.

## Support
If you have any issues or feature requests, please file them in the [GitHub issues](https://github.com/miki4920/party-equipment-analyzer/issues) for this repository.

## License
This project is licensed under the [MIT License](LICENSE).

---

We hope you find this application useful for your games. Happy gaming!
