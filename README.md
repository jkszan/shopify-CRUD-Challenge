
# Shopify CRUD System

Good morning / afternoon and thank you for taking the time to look at the README, this submission is implemented as a REST API using Flask, Swagger for API Documentation and frontend interface, and PostgreSQL for storage.

This project has two separate distributions:

1. (Preferred) A Dockerized Service which uses Compose to spin up and populate a local PostgreSQL instance on startup.

2. A simplified version of this application uploaded onto Replit using Elephant SQL to host PostgreSQL as a service.

The Docker app requires an OpenWeatherAPI key and requires some setup but is very stable and configurable, the Replit app has worse performance but is ready with the click of a button.



## Solution Scope

This is meant to operate as a demo application to give reviewers a general idea of my ability to create a backend application. In a production application I would have included:

- Automated unit test suites

- Much more inline documentation and help strings

- Request handling and scalable parallel workers through Redis

- A proper networking solution such as uWSGI or Waitress

- More data tables such as "User" or "Company" for inventory / item ownership

- CRUD operations implemented where applicable on all tables

- Proper web interfaces for different use-cases as opposed to just the Swagger UI platform.

- A more sophisticated deployment process using Ansible to instantiate instances remotely

While I could have created a CRUD app for items using a single large "item" table but to simulate this being a component in a larger system I have made a small database schema.

<br />

### **Additional Requirements:**
For this submission, the requirement I've chosen is:
- The Ability to create warehouses/locations and assign inventory to specific locations

This has been implemented in the form of the relationship between the items table, the inventory table, and the address table. The inventory table works as both a specific location that items can be assigned to that has a linked address and a logical grouping of items with attached metadata such as "name", "owner", and "size".

Originally this solution had an additional "location" table between address and inventory but it ended up having very few pieces of relevant data that couldn't be more naturally placed in either of it's related tables. In the future a location table could be recreated with a location_type enum (i.e. 'Warehouse') and/or a long form location description if this data is required. Currently you can approximate these values through the inventory_name variable (i.e. 'Production Engineer Warehouse')

<br />

## Requirements and Usage Instructions

### **Docker app Requirements and Installation:**

Requirements:
- Docker
- An Open Port (Default 5000)
- OpenWeatherAPI API Key

To install Docker on your machine, follow the official instructions at https://docs.docker.com/get-docker/.



To alter configuration variables passed to the containers (And provide an API Key) you can edit the variables within the included.env file. If you do not have an OpenWeatherAPI key you can generate one at https://home.openweathermap.org/users/sign_up.



To start the application, run:

 docker compose up --build

From the root of the Github repo

<br />

### **Usage:**
By default the REST API should be available at http://localhost:5000 or https://shopify-crud-system.jkszan.repl.co/ depending on which distribution you are using, you can either call the endpoints directly or use the provided Swagger UI interface.

To use the Swagger UI interface you need to click an endpoint, press the "Try it out" button, insert query parameters, and then press the "Execute" button at the bottom. The response will appear below the "Execute" button.



<br />

## Database Relations and Starting Demo Data

In both the Dockerized version and the Replit version the schema is initiated automatically and some pieces of data are added for test.

You can refresh this data in the Docker App by deleting the data volume and recreating the database container with Compose.

Except for item, all of these tables automatically create IDs using Postgres Identities.

[Full Diagram](./DB_Diagram.pdf)




### **Item Table:**
- The central table of this application, holds information about a specific physical item

| Serial Number | Inventory | Product | Condition | Damage Description |
| :---: | :---: | :---:| :---: | :---: |
| 2312412 	| 2 | 1 | Refurbished 	| Like New		|
| 2424444 	| 3 | 2 | Used 			| Weak magnet 	|
| 2142444 	| 1 | 3 | New 			| 				|



### **Product Table:**

- Holds information about a model of item in storage



| Product ID | Product Name | Product Brand | Product Description |
| :---: |:---:| :---:| :--- |
| 1 | Pixel 6                   | Google    | Dual rear camera system: 50 MP wide 12 MP ultra wide 	|
| 2 | Rambler® 30 oz Tumbler    | Yeti      | Iced coffee, sweet tea, lemonade, water, you name it, you’re set. Fits in most cupholders.|
| 3 | Anti-Dust Chalk Sticks    | Crayola   | Crayola Anti-Dust Chalk sticks keep dust to a minimum and are perfect for writing and drawing on blackboards. Available in white.|



### **Inventory Table:**

- Store information on a specific inventory
- Owner could be an organization or individual, potentially a foreign key to a separate table

By not tying a item directly to an address we can provide more granular information on what an item's purpose in storage is and group them together more logically.

| Inventory ID | Address ID | Inventory Name | Owner | Size |
| :---: |:---:| :---:| :---: | :--- |
| 1 | 1 | Backend Storage   | Alex Placeholder  | (Generated) |
| 2 | 2 | Frontend Storage  | Jerry Placeholder | (Generated) |
| 3 | 3 | Vancouver Storage | Linda Placeholder | (Generated) |




### **Address Table:**

- Stores addresses
- Could be used elsewhere in a bigger system (i.e. Employee or Company Address)

| Address ID | Address Country | Address State | Address City | Street Name | House Number | Apt Specifier | Postal Code |
| :---: |:---:| :---:| :---: | :--- | :---: | :---: |:---: |
| 1 | Canada | ON | Ottawa      | O'Connor St       | 151   |       | K2P 2L8 |
| 2 | Canada | ON | Ottawa      | Laurier Ave W     | 234   | #500  | K2P 2L8 |
| 2 | Canada | ON | Vancouver   | Langmuir Street   | 1055  |       | V7X 1L3 |