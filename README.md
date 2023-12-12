# T2A2 API Web Server Project

### Student: Deandre Sugandhi

[Github Repository](https://github.com/deandresugandhi/DeandreSugandhi_T2A2)

## Table of Contents

## R1 - Identification of the problem you are trying to solve by building this particular app

The purpose of this app is to assist people trying to find and retrieve items they have lost, especially in establishments where this may occur more often, such as train stations, buses, printing stations / internet cafes (leaving USBs / other portable storage devices in the computers), supermarkets, and cinemas, as well as in 'unowned' spaces which may not have a dedicated lost-and-found facility, such as public roads, highways, sidewalks, bus stops, public toilets, some recreation areas, public markets, and open plazas.

This app will be designed so that it can be used flexibly as a solution to various problems. For example, it can be used as a tool for establishment to improve their own lost-and-found facilities, or maybe developed into an independent community website for items lost in unowned public spaces.

## R2 - Why is it a problem that needs solving?

While many places usually have dedicated lost-and-found facilities, where staffs keep reliable records of lost items and store them safely for people to retrieve later, based on my experience, people will usually need to contact these establishments through phone or email to find out if the items they have lost are there. This may be inefficient for both parties at times; for example, busy establishments and their staffs may take longer to respond to such emails, or to pick up such calls, only for the callers to possibly discover that their items are not there or that they may have misplaced their items elsewhere.

Furthermore, while dealing with people claiming their lost items may require more personal verification methods such phone calls or face-to-face meetings, dealing with people just trying to find out if their lost items are kept in an establishment's lost-and-found section does not necessarily require such verification measures; thus it can be argued that records of such items should be made more accessible, such as by displaying them in websites. Thus, this app can potentially eliminate unnecessary work for staffs who need to respond to inquiries on lost items which may not even be left there, and make it more convenient for people to trace their lost items.

Another problem this app can address is for items that are lost in 'unowned' spaces such as public roads, highways, sidewalks, bus stops, public toilets, some recreation areas, public markets, open plazas, etc., which may not have dedicated lost-and-found facilities. A person finding someone else's possibly misplaced items in such places, especially ones with no identifications, may not be sure what to do with them. For example, moving them to a safer, more hidden location can possibly cause more confusion for the owner of the items if they immediately retrace their steps and come back for it. Turning it in to a nearby establishment / local authorities can be similarly confusing for both parties especially if there are multiple establishments / authorities nearby. On the other hand, leaving them where they are leaves them open to thieves. This app can make it easier for these people to make a decision; they can make a post in the web app, noting which establishment they have turned these items to, or even their own contact information if they decide to hold the items temporarily for safekeeping.

## R3 - Why have you chosen this database system? What are the drawbacks compared to others?

I have chosen to use PostgreSQL as the database management system for this app. 

One reason for this decision is its robustness. PostgreSQL is an ACID-compliant (Atomicity, Consistency, Isolation, Durability) DBMS, ensuring all database transactions are processed in a reliable way that prioritizes data integrity (Singh, 2023). Some of its built-in data integrity mechanisms include data types, triggers, and constraints. Furthermore, its write-ahead logging, according to Peterson (2023), also makes it a fault tolerant DBMS that minimizes the risk of data loss. Data integrity is particularly important for something like a lost-and-found system, whose main purpose is to accurately manage and record data on the lost items in order to minimize the difficulties of reporting, finding, and retrieving lost items. PostgreSQL's features such as constraints also ensure that items are categorized and named accordingly, making search functionalities more reliable for people finding their lost items.

Another reason for choosing PostgreSQL is its performance and scalability. It supports various performance optimization such as unrestricted concurrency and geospatial support, making it efficient as the lost-and-found database grows (IBM, n.d.). Its support for geospatial data types with its powerful extensions may also prove to be useful as the app is developed further, as a lost-and-found system would benefit greatly from having detailed geographical information on the items (such as where they are found and where they are currently located) that are managed efficiently. Furthermore, PostgreSQL is a mature and widely adopted DBMS; it existed since the 1990s and have been developed ever since as an open-source software with a large and active community, becoming one of the most popular DBMS (Bollhoff, 2023; Panchenko, 2021).

However, its extensibility can also become its weakness; according to Kolovson (2021), PostgreSQL can have 'too many moving parts' which can become very complex to set up and maintain. This makes it inconvenient to be used in, for example, embedded applications, such as virtual machines or containers (Kolovson, 2021).

Furthermore, its open-source nature also means that because it not owned by a single vendor, users need to navigate through multiple choices of vendors and solutions to perform certain functions, requiring knowledge and understanding of the benefits and drawbacks of each (Panchenko, 2021).

PostgreSQL also has designs to make it easier to operate. Its transactional DDL (Data Definition Language) such as functions to create table or drop table in a single transaction makes managing complex relational applications more convenient (Davidson, 2022; Dhruv, 2023). Its system view, according to Davidson (2022) is also complete and easy to monitor.

## R4 - Identify and discuss the key functionalities and benefits of an ORM

## R5 - Document all endpoints for your API

## R6 - An ERD for your app

![ERD](./docs/images/ERD.png)

## R7 - Detail any third party services that your app will use

### Flask

### SQL Alchemy

### Marshmallow

### Psycopg2

### Bcrypt

### JWT Manager

## R8 - Describe your projects models in terms of the relationships they have with each other

### User model

The User model represents a user record in the database. It has one-to-many relationships with the ItemPost and Comment models, meaning that a user can be associated with multiple item posts and comments as their owner, but each item post and comment stored in the database can only have one user as its original owner. To define this relationship, user_id is used as a foreign key in the ItemPost and Comment models. The cascade deletes ensure that all comments and item posts owned by a user is also removed from the database when that user is deleted.

### Location model

The Location model represents an address used in the app. It has one-to-many relationships with the ItemPost model, meaning that each location can be associated with multiple item posts, while each item post can only refer to one location record. In this case, however, each item post is linked to up to two location records, as an item post has two attributes linked to the Location model defined by the foreign keys in the __ItemPost__ model named __seen_location_id__ and __pickup_location_id__, both referring to the __location_id__ primary key of the __Location__ model. Further details will be explained in the __ItemPost__ model section.

### ItemPost model

The ItemPost model represents an item post record in the database. It has multiple relationships with multiple models. Firstly, it has a many-to-one relationship with the User model, meaning that a user can own multiple item posts but an item post can only have one user associated with it as its owner. This relationship is defined by using user_id as a foreign key in the ItemPost model.

Secondly, it has a one-to-many relationship with the Comment and Image model, since an item post can have multiple comments / images posted to it, while each comment / image can only be associated with one item post. This relationship is defined by using item_post_id as a foreign key in both the Comment and Image model. The cascade deletes ensure that the comments and images associated with an item post are also removed from the database when that item post is deleted.

Thirdly, it has a many-to-one relationship with the Location model. There are two attributes in the ItemPost model that refers to records in the Location model, namely seen_location_id (refers to the location in which the item was found or lost) and pickup_location_id (refers to the location in which the item can / requested to be picked up). These two are foreign keys in the ItemPost model referring to location_id in the Location model, defining this relationship. Each item post can only have one seen location and pickup location, while each location can be associated with multiple item posts.

### Comment model

The Comment model represents a comment posted on an item post. It has many-to-one relationships with the ItemPost and User models. A user can create multiple comments across multiple item posts, while each comment can only be owned by one user. Similarly, an item post can contain multiple comments posted into it, but a comment can only be associated with one item post, i.e. the item post in which it was posted. The relationship is defined through the inclusion of user_id (primary key of the User model) and item_post_id (primary key of the ItemPost model) as foreign keys in the Comment model.

It also has a one-to-many relationship with the Image model, as users can attach multiple images into their comments, with each image record stored in the database associated with only one comment / item_post. This relationship is defined by the comment_id foreign key (referring to the primary key of the Comment model) in the Image model.

### Image model

The Image model represents an image that is attached to either an item post or comment. It forms many-to-one relationships with the ItemPost and Comment models, as a user can attach multiple images into their item posts / comments, while each image can only be associated with one item post / comment. These relationships are defined by using comment_id (primary key of the Comment model) and item_post_id (primary key of the ItemPost model) as foreign keys in the Image model. A constraint is defined using SQLAlchemy's CheckConstraint class with XOR operator to specify that an image can only be associated with one of either an item post or comment, but not both.

## R9 - Discuss the database relations to be implemented in your application

For the purpose of this application, a PostgreSQL database named "lost_and_found_db" is created. To implement the relations and their relationships with one another, 5 tables are created in the database, namely users, item_posts, comments, images, and locations. The interaction between the records in these 5 relations will determine the main functionalities and behavior of the app.

### Users

User-related information are stored in the __users__ table. Each record in the table represents a registered user in the application, with information on their name, username, email, hashed password, admin rights, and their unique ID (the primary key).

### Item Posts

Item posts-related information are stored in the __item_posts__ table. Each record in the table represents an item post that have been posted into the system, with information on its title, post type (whether the user "found" or "lost" the item in the post), item category, item description, retrieval description (brief on how the item can be claimed, such as contact details or locations), item status (such as "claimed" or "unclaimed"), the date in which the post is created, the user who made the post (using a __user_id__ foreign key), seen location (the location in which the item is lost or found, using a __seen_location_id__ foreign key referring to a __location__ record), pickup location (the location in which the item can be claimed, using a __pickup_location_id__ foreign key referring to a __location__ record), and its unique ID (the primary key). As a result, a __user__ can be associated with multiple __item posts__, and an __item_post__ can be associated with up to two __location__ records.

### Comments

Comment-related information are stored in the __comments__ table. Each record in the table represents a comment 

## R10 - Describe the way tasks are allocated and tracked in your project