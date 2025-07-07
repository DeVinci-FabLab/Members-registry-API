# Project Documentation: `members-registry-api`

**Author:** DeVinci Fablab  
**Date:** 07/02/2025

---

## Table of Contents

- [Project Documentation: `members-registry-api`](#project-documentation-members-registry-api)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [Project Overview](#project-overview)
    - [Motivation](#motivation)
  - [System Architecture](#system-architecture)
    - [Overview](#overview)
    - [Technologies Used](#technologies-used)
  - [Data Model](#data-model)
    - [Member: Main Attributes](#member-main-attributes)
    - [Member Status](#member-status)
    - [Promotion](#promotion)
    - [Roles](#roles)
    - [Contribution](#contribution)
    - [Internal Regulation (IR)](#internal-regulation-ir)
    - [Training](#training)
  - [Installation and Setup](#installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Usage](#usage)
    - [Main Features](#main-features)
    - [Running the Application](#running-the-application)
    - [API Endpoints / Features](#api-endpoints--features)
  - [Code Structure](#code-structure)
    - [Folder Organization](#folder-organization)
    - [Key Modules](#key-modules)
  - [Testing](#testing)
    - [Testing Strategy](#testing-strategy)
    - [Running Tests](#running-tests)
  - [Contributing](#contributing)
  - [References](#references)

---

## Introduction

### Project Overview

This project, called `members-registry-api`, aims to provide a modern and secure API for managing Fablab members. The main goal is to centralize, structure, and automate the management of registrations, statuses, promotions, contributions, and access, while ensuring data traceability and security. This API also facilitates integration with other digital tools used by the association.

### Motivation

Manual management of members and related information (statuses, contributions, roles, etc.) is often a source of errors, wasted time, and lack of visibility for association managers. This project addresses the need to automate and secure these processes, while offering a modern, secure, and easily extensible interface. It is part of a continuous improvement approach for the organization and associative life within the Fablab.

---

## System Architecture

### Overview

The project architecture is based on a clear separation of responsibilities and a modular approach:

- **API Backend (FastAPI):** Main entry point for all requests. Handles business logic, data validation (Pydantic), authentication, and exposes REST endpoints.
- **Database (PostgreSQL):** Stores all structured data (members, statuses, promotions, contributions, roles, etc.). Accessed via SQLAlchemy for object-relational mapping.
- **Migrations Management (Alembic):** Allows controlled and reproducible evolution of the database schema.
- **Containerization (Docker):** Facilitates deployment and execution in any environment by isolating dependencies.
- **Automated Testing (pytest):** Ensures code reliability and non-regression.

**Main flow:**  
The user (or an external service) interacts with the API via HTTP. The API processes the request, performs the necessary operations on the database, and returns a structured response (usually in JSON format).

**Simplified diagram:**

```
Client <-> FastAPI (Backend) <-> PostgreSQL
```

*Tools like Docker, Alembic, and pytest are used for deployment, maintenance, and code quality monitoring.*

### Technologies Used

The project relies on a robust and proven tech stack, organized as follows:

- **Programming Language**
  - **Python:** Main language for API development, known for its readability and large community.

- **Backend Frameworks and Libraries**
  - **FastAPI:** Modern, high-performance web framework for building REST APIs, with automatic documentation and async support.
  - **Pydantic:** Data schema validation and serialization.
  - **SQLAlchemy:** ORM for easy interaction between Python and the relational database.
  - **Alembic:** Database migration management.

- **Database**
  - **PostgreSQL:** Reliable, high-performance open-source relational database system.

- **Containerization and Deployment**
  - **Docker:** Application containerization for portability, reproducibility, and easy deployment.
  - **Docker Compose:** Multi-container orchestration for launching the entire stack.

- **Testing and Quality**
  - **pytest:** Unit testing framework to ensure code quality.

- **Version Control and Collaboration**
  - **Git:** Source code version control.
  - **GitHub:** Hosting platform, issue management, and continuous integration.

- **Additional Tools**
  - **.env:** Environment variable management for secure configuration.

- **Authentication and Security**
  - **OAuth2 / JWT (JSON Web Token):** Secure authentication and user session management via tokens.
  - **python-jose:** JWT token generation and validation.
  - **Passlib:** Secure password hashing library (e.g., bcrypt).
  - **FastAPI Dependencies:** Role, scope, and authorization control via the dependency system (`Depends()`).
  - **Permission Management:** Role-based access control for securing sensitive routes.
  - **Input Validation (Pydantic):** Protection against injections and strict data validation.

---

## Data Model

![UML](./img/register_database_schema.png)

### Member: Main Attributes

Each member is defined by the following attributes:

- **id:** *int* <<PK>> — Unique member identifier.
- **last_name**, **first_name:** *varchar* — Member's last and first names.
- **present:** *bool* — Current presence in the association.
- **arrival**, **departure:** *date* — Arrival and departure dates.
- **email**, **personal_email:** *varchar* — Institutional and personal emails.
- **phone**, **discord:** *varchar* — Contact details.
- **trainers:** *varchar* — Indicates in which field the member is a trainer.
- **notes:** *varchar* — Comments or various notes.
- **srg:** *bool* — Indicates if the member has completed the SRG.
- **warning:** *int* — Number of warnings received.
- **created_by**, **modified_by:** *varchar* — Identifiers of users who created or modified the record.
- **created_at**, **modified_at:** *date* — Creation and last modification dates.
- **convs**, **portal:** *bool* — Added on discord and portal.
- **status_id**, **promotion_id:** *int* <<FK>> — References to related tables (status, promotion).

### Member Status

A member's status determines their rights and level of involvement. Possible statuses include:

- **Annual Member:** Standard member for the current year.
- **Founding Member:** Participant in the creation of the association.
- **Control Committee Member:** Member of the supervisory committee.
- **Honorary Member:** Honorary distinction.
- **Emeritus Member:** Former member recognized for their commitment.
- **Pending:** Registration pending validation.
- **Removed:** Member excluded from the association.
- **Persona Non Grata:** Explicitly banned member.

### Promotion

Each member is linked to a promotion, defined by:

- **school:** Name of the school (e.g., ESILV)
- **year:** Promotion year (e.g., 2024)
- **level:** Study level (e.g., A3)
- **apprentice:** *bool* — Indicates if the member is an apprentice
- **major:** Major (e.g., MMN)

*Example:*

```json
{
  "school": "ESILV",
  "year": 2024,
  "level": "A3",
  "apprentice": true,
  "major": "MMN"
}
```

### Roles

Roles structure the internal organization. A member can have multiple roles or none.

- **CODIR:** President, Vice Presidents, General Secretary, Treasurer
- **CG:** Department heads (e.g., Communication, Events, Training, etc.)
- **CHARGE:** Specific functions (e.g., DD RSE, VSS, PSC1, etc.)

### Contribution

A member's contribution reflects their financial status with the association:

- **Paid:** Contribution paid for the current year.
- **Due:** Contribution to be paid.
- **Exempt - Status:** Exemption due to member status.
- **Exempt - Removed:** Exemption due to removal.
- **Exempt - PNG:** Exemption due to ban.

### Internal Regulation (IR)

Internal regulation tracking for each member:

- **Signed:** IR signed by the member.
- **To renew:** IR signature to be renewed.
- **Exempt - Status:** Exemption due to status.
- **Exempt - Removed:** Exemption due to removal.
- **Exempt - PNG:** Exemption due to ban.

### Training

Tracks training sessions attended by members:

- **name:** Name of the training
- **description:** Description of the training
- **participation_date:** Date of participation
- **status:** Status of participation

---

## Installation and Setup

### Prerequisites

List the required software and dependencies.

### Installation Steps

Provide step-by-step instructions to install the project.

---

## Usage

### Main Features

The API provides the following features for managing Fablab members:

- **Authentication and access management:**
  - Secure user authentication (OAuth2/JWT).
  - Permission and access management based on roles.
- **Full CRUD on main entities:**
  - Create, read, update, and delete members, promotions, statuses, roles, contributions, etc.
- **History and traceability:**
  - Track changes and actions performed on members (audit, logs).
- **Statistics and reporting:**
  - Generate statistics on members (by status, promotion, role, etc.).
  - Export reports for association activity tracking.
- **Advanced search and filtering:**
  - Multi-criteria search on members (name, status, promotion, role, etc.).
  - Dynamic filters for easier management and analysis.
- **Integration with external tools (e.g., Discord bot):**
  - Automatic assignment of roles or rights via bots (e.g., Discord role assignment based on status or promotion).
  - Data synchronization with other digital platforms.

### Running the Application

Explain how to run or deploy the project.

### API Endpoints / Features

Document the main API endpoints or features.

---

## Code Structure

### Folder Organization

Describe the main folders and files.

### Key Modules

Explain the purpose of important modules or classes.

---

## Testing

### Testing Strategy

Describe how the project is tested.

### Running Tests

Explain how to run the tests.

---

## Contributing

Provide the rules for contributing to the project.

---

## References

List references,
