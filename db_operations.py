#!/usr/bin/env python3
"""
Database operations module for handling user, job, and application interactions.

This module contains functions for registering users, managing jobs, and handling job applications
using SQLAlchemy ORM for database operations.

Modules imported:
- flask.jsonify: For converting Python dictionaries to JSON responses.
- sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.IntegrityError: Exception classes for database errors.
- base.SessionLocal: Provides a local session for database operations.
- models.user.User, models.job.Job, models.application.Application: SQLAlchemy model classes for User, Job, and Application entities.
- sqlalchemy.orm.exc.NoResultFound, sqlalchemy.orm.exc.MultipleResultsFound: Exceptions raised when querying with SQLAlchemy ORM.

Functions:
- register_user(username, password, email, role, phone_number, address, first_name=None, last_name=None,
                company_name=None, website=None, contact_info=None):
  Registers a new user in the database with provided details.

- login_user(email, password):
  Retrieves a user from the database by email and verifies the password.

- get_user_by_id(id):
  Retrieves a user from the database by their ID.

- get_all_users():
  Retrieves all users from the database.

- get_all_jobs():
  Retrieves all jobs from the database.

- create_job(data):
  Creates a new job in the database with provided details.

- get_job_by_id(job_id):
  Retrieves a job from the database by its ID.

- get_jobs_by_employer_id(employer_id):
  Retrieves all jobs posted by a specific employer.

- update_job(job_id, data):
  Updates a job in the database with provided data.

- delete_job(job_id):
  Deletes a job from the database by its ID.

- create_application(data):
  Creates a new job application in the database with provided data.

- get_applications(user_id, role):
  Retrieves applications based on user ID and role (employer or job seeker).

- get_application_by_id(application_id):
  Retrieves a job application from the database by its ID.

- update_application_status(application_id, data):
  Updates the status of a job application in the database (restricted to employers).

- delete_application(application_id):
  Deletes a job application from the database by its ID.
"""

from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from base import SessionLocal
from models.user import User
from models.job import Job
from models.application import Application
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


"""user database operations"""

def register_user(username, password, email, role, phone_number, address,
                 first_name=None, last_name=None, company_name=None, website=None, contact_info=None):
    """
    Register a new user in the database.

    Args:
    - username (str): The username of the new user.
    - password (str): The plain text password of the new user.
    - role (str): The role assigned to the new user.
    - email(str): The email of the new user.
    - company_name(str): The company name for employers.
    - phone_number(str): Contact details of the user.
    - address(str): Address of the user.
    - first_name(str): The name of the job_seeker.
    - last_name(str): The last name of the job_seeker.
    - website(str): The website of the employer.
    - contact_info(str): The contact details of the employer.

    Returns:
    - None

    Raises:
    - SQLAlchemyError: If there's an error during the database transaction.

    This function hashes the provided plain text password using `generate_password_hash`,
    creates a new `User` object with the provided username, hashed password, and role, 
    and then adds this new user to the database session and commits the transaction.
    """
    new_user = User(
        username=username,
        email=email,
        role=role,
        phone_number=phone_number,
        address=address,
        first_name=first_name,
        last_name=last_name,
        company_name=company_name,
        website=website,
        contact_info=contact_info
    )

    """Validate role-specific fields."""
    try:
        new_user.validate_role_specific_fields()
    except ValueError as ve:
        raise ValueError(f"Validation error: {str(ve)}")

    print(f"Debugging new_user fields: {new_user.__dict__}")

    """Harsh the password and set."""
    new_user.set_password(password)
    """Add the new user to the database session and commit the transaction."""
    session = SessionLocal()
    try:
        session.add(new_user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise SQLAlchemyError(f'Failed to register user: {str(e)}')
    finally:
        session.close()


def login_user(email, password):
    """
    Retrieve a user from the database by their email address and validate the password.

    Args:
    - email (str): The email address of the user to retrieve.
    - password (str): The plain text password to verify.

    Returns:
    - User: The user object if login is successful.
    - None: If no user is found with the given email or password does not match.

    Raises:
    - SQLAlchemyError: If there's an error during the database query.

    This function queries the database for a user with the provided email address.
    If found, it verifies the provided password against the stored password hash.
    If both email and password are correct, it returns the user object.
    """
    try:
        session = SessionLocal()
        user = session.query(User).filter_by(email=email).one()
        if user.check_password(password):
            return user
        else:
            return None
    except NoResultFound:
        return None
    except MultipleResultsFound:
        return None
    except SQLAlchemyError:
        return None

 
def get_user_by_id(id):
    """
    Retrieves a user by their ID from the database.

    Args:
    - id (int): The ID of the user to retrieve.

    Returns:
    - User: The user object if found.
    - None: If no user is found with the given ID.

    Raises:
    - NoResultFound: Exception when no user is found with the given ID.
    """
    try:
        session = SessionLocal()
        user = session.query(User).get(id)
        return user
    except NoResultFound:
        return None

def get_all_users():
    """Retrieve all users from the database."""
    session = SessionLocal()
    users = session.query(User).all()
    return [user.to_dict() for user in users]


"""Define Job database operations."""


def get_all_jobs():
    """
    Retrieve all jobs from the database.

    Returns:
        list: A list of dictionaries representing each job, or None if there's an error.
    """
    try:
        session = SessionLocal()
        jobs = session.query(Job).all()
        jobs_list = [job.to_dict() for job in jobs]
        return jobs_list
    except Exception as e:
        print(f"Error retrieving jobs: {str(e)}")
        return None


def create_job(data):
    """
    Create a new job in the database.

    Args:
        data (dict): A dictionary containing job details.

    Returns:
        int or None: The ID of the newly created job if successful, None otherwise.
    """
    try:
        new_job = Job(
            title=data['title'],
            description=data['description'],
            requirements=data['requirements'],
            employer_id=data['employer_id'],
            salary=data['salary'],
            location=data['location'],
            job_type=data['job_type'],
            application_deadline=data['application_deadline'],
            skills_required=data['skills_required'],
            preferred_qualifications=data['preferred_qualifications']
        )
        session = SessionLocal()
        session.add(new_job)
        session.commit()
        return new_job.id
    except Exception as e:
        session.rollback()
        print(f"Error creating job: {str(e)}")
        return None


def get_job_by_id(job_id):
    """
    Retrieve a job from the database by its ID.

    Args:
        job_id (int): The ID of the job to retrieve.

    Returns:
        dict or None: A dictionary representing the job details if found, None otherwise.
    """
    try:
        session = SessionLocal()
        job = session.query(Job).get(job_id)
        if job:
            return job.to_dict()
        else:
            print(f"Job with ID {job_id} not found.")
            return None
    except SQLAlchemyError as e:
        print(f"Error retrieving job {job_id}: {str(e)}")
        return None


def get_jobs_by_employer_id(employer_id):
    """
    Retrieve all jobs posted by a specific employer.

    Args:
        employer_id (int): The ID of the employer.

    Returns:
        list: A list of dictionaries representing each job, or None if there's an error.
    """
    try:
        session = SessionLocal()
        jobs = session.query(Job).filter_by(employer_id=employer_id).all()
        jobs_list = [job.to_dict() for job in jobs]
        return jobs_list
    except SQLAlchemyError as e:
        print(f"Error retrieving jobs for employer {employer_id}: {str(e)}")
        return None
    finally:
        session.close()


def update_job(job_id, data):
    """
    Update a job in the database.

    Args:
        job_id (int): The ID of the job to update.
        data (dict): A dictionary containing updated job details.

    Returns:
        bool: True if the job was successfully updated, False otherwise.
    """
    try:
        session = SessionLocal()
        job = session.query(Job).get(job_id)
        if job:
            job.title = data['title']
            job.description = data['description']
            job.requirements = data['requirements']
            job.salary = data['salary']
            job.location = data['location']
            job.job_type = data['job_type']
            job.application_deadline = data['application_deadline']
            job.skills_required = data['skills_required']
            job.preferred_qualifications = data['preferred_qualifications']
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating job {job_id}: {str(e)}")
        return False


def delete_job(job_id):
    """
    Delete a job from the database along with any related applications.

    Args:
        job_id (int): The ID of the job to delete.

    Returns:
        bool: True if the job was successfully deleted, False otherwise.
    """
    try:
        session = SessionLocal()
        job = session.query(Job).get(job_id)
        if job:
            """Delete related applications if necessary"""
            related_applications = session.query(Application).filter(Application.job_id == job_id).all()
            for application in related_applications:
                session.delete(application)
            
            session.delete(job)
            session.commit()
            return True
        else:
            print(f"Job with ID {job_id} not found.")
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting job {job_id}: {str(e)}")
        return False
    finally:
        session.close()


"""Application endpoints."""


def create_application(data):
    """
    Create a new application for a job in the database.

    Args:
    - data (dict): A dictionary containing application details.

    Returns:
    - Application: The created application object if successful.
    
    Raises:
    - ValueError: If the user has already applied for the job.
    """
    session = SessionLocal()

    """Check if the user has already applied for this job."""
    existing_application = session.query(Application).filter_by(user_id=data['user_id'], job_id=data['job_id']).first()
    if existing_application:
        raise ValueError("You have already applied for this job")

    application = Application(
        job_id=data['job_id'],
        employer_id=data['employer_id'],
        user_id=data['user_id'],
        years_of_experience=data.get('years_of_experience'),
        resume=data['resume'],
        cover_letter=data['cover_letter'],
        status=data['status'],
        name=data['name'],
        school_name=data['school_name'],
        portfolio=data['portfolio'],
        skills=data['skills']
    )
    session.add(application)
    session.commit()
    return application


def get_applications(user_id, role):
    """
    Retrieve applications based on user ID and role.

    Args:
    - user_id (int): The ID of the user whose applications to retrieve.
    - role (str): The role of the user ('employer' or 'job_seeker').

    Returns:
    - list: A list of Application objects filtered by user ID and role, or an empty list if no applications found.
    
    Raises:
    - Exception: Any exception raised during database query.
    """
    session = SessionLocal()
    try:
        if role == 'employer':
            return session.query(Application).filter_by(employer_id=user_id).all()
        return session.query(Application).filter_by(user_id=user_id).all()
    except Exception as e:
        raise e
    finally:
        session.close()
    

def get_application_by_id(application_id):
    """
    Retrieve an application by its ID from the database (restricted to employers).

    Args:
    - application_id (int): The ID of the application to retrieve.

    Returns:
    - Application: The Application object if found, None if no application found.
    
    Raises:
    - Exception: Any exception raised during database query.
    """
    session = SessionLocal()
    try:
        return session.query(Application).get(application_id)
    except Exception as e:
        raise e
    finally:
        session.close()


def update_application_status(application_id, data):
    """
    Update the status of an application in the database (restricted to employers).

    Args:
    - application_id (int): The ID of the application to update.
    - data (dict): A dictionary containing the updated status.

    Returns:
    - dict: The updated Application object as a dictionary if successful, None if application not found.
    """
    session = SessionLocal()
    try:
        application = session.query(Application).get(application_id)
        if not application:
            return None
        if 'status' in data:
            application.status = data['status']
        session.commit()
        application_dict = application.to_dict()  # Convert to dictionary before closing session
        return application_dict
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating application {application_id}: {str(e)}")
        return None
    finally:
        session.close()


def delete_application(application_id):
    """
    Delete an application from the database (restricted to employers).

    Args:
    - application_id (int): The ID of the application to delete.

    Returns:
    - bool: True if the application was successfully deleted, False otherwise.
    
    Raises:
    - Exception: Any exception raised during database query or commit.
    """
    application = get_application_by_id(application_id)
    if not application:
        return False
    session = SessionLocal()
    session.delete(application)
    session.commit()
    return True
