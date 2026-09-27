# Vehicle Rental API

A modern, production-ready RESTful API for a vehicle rental system built with Python, FastAPI, and SQLAlchemy. This project demonstrates clean architecture patterns, separation of concerns, and containerization.

## Features

- **User Management**: Create, read, and validate users.
- **Vehicle Fleet Management**: Add, list, and delete vehicles with real-time availability tracking.
- **Booking System**: Handle vehicle reservations, prevent double-bookings, and automatically calculate total rental payments.
- **Data Filtering**: Dedicated endpoints for checking instantly available vehicles.

## Tech Stack

- **Framework**: FastAPI (Asynchronous, high performance)
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic v2
- **Environment**: Docker & Uvicorn

## Architecture & Best Practices

This project was built following industry-standard patterns to ensure maintainability and scalability:
- **Separation of Concerns**: API routes (`main.py`) act purely as HTTP controllers, delegating all database operations to a dedicated persistence layer (`crud.py`).
- **Data Encapsulation**: Pydantic schemas decouple database models from the API request/response payloads, protecting sensitive data.
- **Dependency Injection**: FastAPI's native dependency injection is used to manage database sessions efficiently per request.
- **Containerization**: Fully dockerized environment for seamless deployment and consistency across machines.

## Getting Started

### Prerequisites

Make sure you have Docker installed on your machine.

### Installation & Run

1. Build and run the application using Docker:
   ```bash
   docker compose up --build
   ```

2. The API will be available at `http://localhost:5000`.

## API Documentation

Once the application is running, you can explore the fully interactive API documentation provided by Swagger UI at:
- **Interactive Docs (Swagger)**: `http://localhost:5000/docs`
- **Alternative Docs (ReDoc)**: `http://localhost:5000/redoc`
