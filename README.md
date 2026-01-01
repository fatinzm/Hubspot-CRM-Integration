# Hubspot CRM Integration - Technical Challenge



This project implements the technical challenge described in the
HubSpot CRM Integration Case Study.

The script demonstrates how to:

+ securely authenticate with the HubSpot API

- create a Contact

* create a Company

+ associate the Contact with the Company

- respect API rate-limiting best practices

## Tech Stack

+ Python 3
- requests
* python-dotenv

## Prerequisites

Before running the script, make sure you have:

1. A HubSpot Developer Account

2. A Test Account (Test Portal)

3. A Private App with the following scopes:

    - crm.objects.contacts

    + crm.objects.companies

## Important HubSpot Setting 

 Automation must be disabled in your HubSpot Test Portal

The following HubSpot automation must be turned OFF:

Create and associate Companies with Contacts
Associate current and newly added Contacts with Companies based on a Contact's email address and a Company's domain

If this automation is enabled, HubSpot will automatically create and associate a Company every time a Contact is created, which results in duplicate company associations.

This script assumes that all associations are handled explicitly via the API.

## Environment Configuration

Create a .env file in the project root.

.env example
HUBSPOT_KEY=pat-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
FIRSTNAME=YourFirstName
LASTNAME=YourLastName


HUBSPOT_KEY
Your HubSpot Private App access token

FIRSTNAME / LASTNAME
Your real first and last name (as required by the challenge)


## Installation

Install dependencies using:

pip install -r requirements.txt

## Running the Script

Run the script with:

python main.py

## What the Script Does
### Step 1: Secure Authentication

  - Reads the HubSpot access token from .env

  + No credentials are hardcoded

### Step 2: Create a Contact

  - Creates a Contact with:

      - a fictional email address

      + your real first and last name

### Step 3: Create a Company

  - Creates a fictional Company:

      - Name: Coding Challenge Company GmbH

      + Domain: coding-challenge-company.com

### Step 4: Associate Contact and Company

  - Associates the Contact with the Company

  - Uses the default Contact ↔ Company relationship, which represents an employee/member relationship as required by the task

## Rate Limiting

To simulate production best practices, the script enforces:

- 200ms delay between every API call

This rate limiting is implemented centrally and applies to all HubSpot API requests.

