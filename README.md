# JobKonnect Backend

- The JobKonnect project aims to solve the issue of connecting tech talent with tech job opportunities efficiently. Current job boards are often cluttered with non-tech jobs, making it difficult for tech professionals to find relevant opportunities.
![JobKonnect Logo](https://raw.githubusercontent.com/TatendaTorerwa/Jobkonnect-backend/09bb0455aaadc4ad9b58f4f0f94af9f070abec19/jobkonnect1.PNG)


## Team
- Tatenda Torerwa - Backend Developer

## Technologies

### Backend
- Python Programming Language
- Flask Framework for mananging API request
- Authentication: Token-based authentication managed by JWT


### Database
- MySQL

### Additional Tools
- PythonAnywhere or Render (for deployment)
- Unittest (for backend testing)
- Postman (for API testing/Documentation)

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL
- Git

###Links

- http://tatenda1998.pythonanywhere.com/ - Backend
- https://jobkonnect-frontend.vercel.app/ - Frontend

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/TatendaTorerwa/Jobkonnect_Backend.git
    cd Jobkonnect_Backend
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv myenv
    source myenv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure the database:
    - Create a MySQL database.
    - Update the config.py file with your database credentials.

5. Run the application:
    ```sh
    python3 -m endpoints
    ```

6. Access the backend locally:

- Using curl:
curl -X GET http://127.0.0.1:5000

- Using a web browser:
Go to http://localhost:5000/


7. Deployment:

8. Testing endpoints:
- Use Postman to test the API endpoints.
- Once you've completed these steps, the backend of DocBooking should be installed, configured, and ready to use both locally and in production.

## API Endpoints Overview (Postman)

https://documenter.getpostman.com/view/33810400/2sA3kUGh41

## Contributing
- We welcome all contributions from the community to improve the JobKonnect_Backend. If you'd like to contribute, please follow these guidelines:

### Bug Reports and Feature Requests
- If you encounter any bugs or have ideas for new features, please open an issue on the GitHub repository. When submitting a bug report, please include detailed information about the issue, including steps to reproduce it if possible.

### Pull Requests
- We encourage you to submit pull requests for bug fixes, improvements, or new features. Before submitting a pull request, please ensure the following:

### Fork the repository and create a new branch for your changes.
- Make sure your code adheres to the project's coding style and conventions.
- Write clear and descriptive commit messages.
- Test your changes thoroughly to ensure they work as expected.
- Update the documentation if necessary.
- Once your changes are ready, submit a pull request to the master branch of the main repository. A project maintainer will review your contribution and provide feedback. Please be patient and responsive to any comments or requests for changes during the review process.
- Thank you for considering contributing to the DocBooking project!

## Related projects

## Licensing
The JobKonnect_Backend project, developed by Tatenda Torerwa at AXL Africa in 2024, is licensed under the MIT License, allowing users to freely use, modify, and distribute the software. The MIT License grants permission without warranty and requires the inclusion of the original copyright notice and permission notice in all copies or substantial portions of the software.
