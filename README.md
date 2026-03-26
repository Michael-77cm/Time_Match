# Time Match

Time Match is a Django full-stack web application for coordinating group availability. It allows users to create an event, share a unique event code, join an event, submit availability, and view notifications related to their planning activity.

This README is written to support both project setup and assessment evidence. It documents the current application on the `main` branch of the repository, where the full Django project is located.

## Project Purpose

The goal of Time Match is to solve a common real-world scheduling problem: finding suitable times for multiple people to meet. Instead of relying on scattered messages, users can manage event participation and time submissions in one place.

## Target Users

- Students planning group meetings
- Friends arranging social events
- Teams coordinating availability
- Anyone who needs a simple shared scheduling tool

## Features

- User registration and login using Django authentication
- Event creation with a unique shareable code
- Join-an-event flow using an event code
- Availability submission by date, start time, end time, and status
- Notification panel for user-specific updates
- Event membership tracking
- Event overview page for joined events


## UX Design Process

### Strategy

The application was designed around a clear user journey:

1. Sign up or log in
2. Create or join an event
3. Submit availability
4. Review event information and notifications

The interface is intended to be simple, predictable, and easy to navigate for first-time users.

### UX Goals

- Keep the scheduling flow short and easy to understand
- Use clear labels and simple form inputs
- Make navigation visible on every page
- Reflect authentication state clearly
- Reduce user friction by using event codes instead of complex invitations

### Front-End Design Decisions

- Semantic HTML is used for document structure, navigation, headings, forms, and links
- A consistent navigation bar gives access to key actions
- Authenticated and unauthenticated users see different navigation options
- Django messages provide immediate feedback after important actions
- Templates and CSS are used to keep presentation consistent across the application

### Accessibility Considerations

- The base template includes the mobile viewport meta tag
- Forms use labels and Django form handling for structured input
- Navigation links are visible and grouped logically
- Content is separated into templates to support consistent layout
- The project should be checked with a WCAG validator before final submission, and screenshots/results can be added below

Accessibility evidence to add before submission:

- *Link to validator or audit tool used*
- *Screenshot of results showing no major WCAG issues*
- *Notes on any fixes made during testing*

### Wireframes and Mockups
- Desktop wireframe:
  ![Wireframe](https://github.com/user-attachments/assets/9d25ccd7-3910-412a-8a5d-bd7d6fa199f2)

- Mobile view: 
![mobileversion](https://github.com/user-attachments/assets/d76654b1-f77a-489e-aaef-bfc9cfa3fd5a)



### Design Changes During Development

Suggested points to document if they apply to your project:

- Navigation was refined so logged-in users see dashboard actions immediately
- Feedback messages were added to improve form clarity
- Event access was simplified by using a shareable event code
- The event flow was split into smaller pages to reduce confusion

## Agile Planning

An Agile tool should be used to plan and track the project. Add the link and screenshots for evidence.

Recommended evidence:

- Project board link: `ADD TRELLO / GITHUB PROJECTS / JIRA LINK`
- Screenshot of backlog: `ADD IMAGE`
- Screenshot of in-progress and completed tasks: `ADD IMAGE`

### Example User Stories

- As a new user, I want to register for an account so that I can create and manage events
- As an authenticated user, I want to create an event so that I can invite others
- As an invited user, I want to join an event using a code so that I can participate quickly
- As an event member, I want to submit my availability so that the group can compare options
- As a user, I want to see notifications about my activity so that I stay informed

## Database Design

The application uses Django ORM with SQLite in development.

### Custom Models

#### `Event`

Stores the event title, unique code, creator, creation timestamp, and optional finalised schedule details.

#### `EventMembership`

Creates a relationship between a user and an event. This ensures a user can join many events and an event can contain many users.

#### `Availability`

Stores a user's submitted date, start time, end time, and availability status for a specific event.

#### `Notification`

Stores short user-specific messages related to event actions.

### Data Relationships diagram
![ERD timewatch](https://github.com/user-attachments/assets/f6e9f4d1-ddb8-41fb-b929-b555afd0d9e3)


### Data Integrity

- `Event.code` is unique
- `EventMembership` uses a uniqueness constraint on `user` and `event`
- Django model fields enforce data types
- Forms use Django validation before data is saved
- Database changes are managed through migrations

## Application Logic

The project includes custom Python business logic in the Django views and forms:

- Event codes are generated using a loop and a uniqueness check
- Conditional logic handles valid and invalid form submissions
- User membership is created only when needed using `get_or_create`
- Form querysets are filtered to show only events relevant to the logged-in user
- Notifications are created automatically after important actions

## CRUD Functionality

### Implemented

- Create event
- Read joined events
- Join event
- Create availability entry
- Read notifications

### Important Note

For a strict interpretation of full CRUD, update and delete views should also be present for at least one core record type before final submission. If you add them, document them here and include screenshots or test evidence.

Suggested CRUD completion options:

- Edit an existing availability record
- Delete an availability record
- Edit an event title
- Delete an event created by the owner

## Forms and Validation

The project includes Django forms for:

- event creation
- joining an event
- availability submission
- user registration through Django's built-in `UserCreationForm`

Validation currently includes:

- required field validation
- event code normalization to uppercase
- event queryset filtering based on the logged-in user
- data-type handling for dates and times

## Authentication, Authorization, and Access Control

### Authentication

- User sign-up is handled through Django authentication
- Login state is reflected in the navigation bar
- Logged-in users see dashboard actions
- Logged-out users see sign-up and login links

### Access Control

- Core dashboard pages use `@login_required`
- Unauthenticated users are redirected away from protected pages
- Users can only submit availability for events they have joined because the form queryset is filtered by membership

### Role-Based Access

The project currently distinguishes between authenticated users and admins through Django's built-in system. If your assessment requires explicit user/admin feature separation in the UI or views, add documentation and screenshots showing admin-specific permissions or protected actions.

## Front-End Implementation

The front end uses Django templates and custom CSS.

Current UI structure includes:

- a shared base template
- page-specific templates
- navigation that changes based on login state
- flash messages for success and error states

Responsive evidence to add before submission:

- screenshots on mobile, tablet, and desktop
- notes on media queries, Flexbox, Grid, or framework usage
- confirmation that no major layout issues occur at smaller widths

## Testing

The repository currently contains a starter `tests.py` file. For assessment, testing evidence should be documented clearly in this README.

### Manual Test Plan

| Feature | Test Case | Expected Result | Actual Result |
| --- | --- | --- | --- |
| Registration | Submit valid sign-up form | User account created and logged in | `PASS` |
| Login | Submit valid credentials | User is logged in and sees authenticated navigation | `PASS` |
| Create Event | Submit event title | Event created with unique code | `PASS` |
| Join Event | Enter valid event code | User is added to event membership | `PASS` |
| Join Event | Enter invalid event code | Clear error message is shown | `PASS` |
| Availability | Submit valid date and time range | Availability saved successfully | `PASS` |
| Notifications | Trigger event creation | User sees notification entry | `PASS` |
| Access Control | Visit protected page while logged out | Redirect to login or denied access | `PASS` |
| Responsiveness | View site on mobile width | Layout remains usable and readable | `PASS` |



## Security

Security-related practices used in the project include:

- storing `SECRET_KEY` in environment variables
- keeping sensitive files out of version control with `.gitignore`
- separating configuration from source code where possible

Before deployment, confirm the following:

- No passwords or secrets are committed
- `DEBUG = False` in production
- production hosts are set correctly
- environment variables are configured on the hosting platform


## Deployment

The project is structured for cloud deployment with `Gunicorn` and a `Procfile`.

- deployed app URL: `https://discord.com/channels/@me/1466753123551940638/1486704188032286720`
- screenshot of deployed home page: `ADD IMAGE`
