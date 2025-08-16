# Crowdfunding Back End

Arsen ILHAN

## Planning:

### Concept/Name

Inkvestor empowers aspiring authors to bring their stories to life.
Readers and supporters can contribute to the books they want to see published, helping writers cover editing, design, and printing costs. If a project reaches its funding goal, the book gets published — turning creative dreams into real pages.

### Intended Audience/User Stories

Our intended audience includes aspiring authors, book lovers, and supporters of creative projects.
Authors will use the website to showcase their book ideas, set funding goals, and connect with potential readers who believe in their work.
Supporters and readers will browse projects, choose the books they want to see published, and contribute funds to help bring those books to life.

### Front End Pages/Functionality

#### Home Page
- Featured fundraising projects (highlighting popular or new campaigns)
- Search and filter options for projects (by genre, funding goal, author, etc.)
- Quick “Support Now” buttons for easy backing
- Links to create a new fundraiser or browse categories

#### Create New Fundraiser Page
- Form with fundraiser details (title, description, funding goal, cover image, sample content)
- Option to set campaign duration and reward tiers
- Ability to preview before submitting
- Submit button to publish the fundraiser
- Nice error pages and inline validation for missing or incorrect details

#### Project Detail Page
- Full description of the book project
- Author profile and background
- Funding progress bar and number of backers
- “Support This Project” section with pledge options
- Comment and Q&A section for backer interaction

#### User Dashboard
- List of fundraisers created by the user
- Funding status and analytics for each project
- Edit or update campaigns (e.g., post news or progress updates)

#### Error / Info Pages
- Custom 404 “Page Not Found” page
- Custom error pages for form validation issues
- Friendly “Thank You” page after a successful pledge or campaign creation


### API Spec

{{ Fill out the table below to define your endpoints. An example of what this might look like is shown at the bottom of the page.

It might look messy here in the PDF, but once it's rendered it looks very neat!

It can be helpful to keep the markdown preview open in VS Code so that you can see what you're typing more easily. }}

different endpoints ( like /fundraisers page pledges, profile etc )

![](./apispec.drawio.svg)

![](./database.drawio.svg)

| URL                       | HTTP Method | Purpose                                           | Request Body                | Success Response Code | Authentication/Authorisation        |
| ------------------------- | ----------- | ------------------------------------------------- | --------------------------- | --------------------- | ------------------------------------ |
| /fundraisers              | GET         | Fetch all fundraisers                             | N/A                         | 200                   | None                                 |
| /fundraisers              | POST        | Create a new fundraiser                           | JSON Payload                | 201                   | Any logged-in user                   |
| /fundraisers/{id}         | GET         | Fetch details of a specific fundraiser            | N/A                         | 200                   | None                                 |
| /fundraisers/{id}         | PUT         | Update an existing fundraiser                     | JSON Payload                | 200                   | Fundraiser owner only                |
| /fundraisers/{id}         | DELETE      | Delete a fundraiser                               | N/A                         | 204                   | Fundraiser owner only                |
| /fundraisers/{id}/pledges | GET         | Fetch all pledges for a specific fundraiser       | N/A                         | 200                   | Fundraiser owner or admin            |
| /fundraisers/{id}/pledges | POST        | Create a pledge for a fundraiser                  | JSON Payload                | 201                   | Any logged-in user                   |
| /profile                  | GET         | Fetch logged-in user profile details              | N/A                         | 200                   | Logged-in user                       |
| /profile                  | PUT         | Update logged-in user profile                     | JSON Payload                | 200                   | Logged-in user                       |
| /auth/register            | POST        | Register a new user                               | JSON Payload                | 201                   | None                                 |
| /auth/login               | POST        | Log in and retrieve authentication token          | JSON Payload                | 200                   | None                                 |
| /auth/logout              | POST        | Log out user and invalidate session/token         | N/A                         | 204                   | Logged-in user                       |






### DB Schema

![]( {{ ./relative/path/to/your/schema/image.png }} )

### Testing Markdown all in one 
``` python
print ("Hello World")

```

``` New line
"My new line testing here" 
You need to start with three ``` and finish with three ```
```