# 🛒 Online Mart - E-commerce Platform

An e-commerce application built using FastAPI, SQLModel, Docker, Kafka, and JWT for authentication. This project includes user authentication, order management, and real-time messaging through Kafka.


# 📖 About the Project

Online Mart is a scalable and secure e-commerce platform with separate services for user authentication and order management. It supports JWT-based authentication, data persistence using SQLModel, and asynchronous event-driven communication using Kafka.

# MicroServices 

- User Service
- Product Service
- Inventory Service 
- Notification Service 
- Order Service 
- Payment Service 

# 🛠️ Technologies Used

- Framework: FastAPI
- Database: SQLModel (SQLite/PostgreSQL)
- Authentication: JWT (JSON Web Token)
- Event Streaming: Kafka
- Containerization: Docker

# 🚀 Getting Started
## 1. Clone the Repository
 
``` git clone https://github.com/Qureshihasaan/Online_mart_Project ```

``` cd Online_mart_Project ```

## 2. Build and run Docker containers:

``` docker compose up --build ```

## 3. Access the API documentation:

#### visit the swagger UI at:
``` http://localhost:8000/docs ```

# 🔧 Environment Variables
### Create a .env file in the root directory with the following:

``` DATABASE_URL=postgresql://user:password@localhost:5432/dbname ```
``` SECRET_KEY=your_secret_key ```
``` ACCESS_TOKEN_EXPIRE_MINUTES=30 ```
``` KAFKA_BROKER=localhost:9092 ```