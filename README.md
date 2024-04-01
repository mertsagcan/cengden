# Cengden

Cengden is a dynamic marketplace platform designed to facilitate the buying, selling, and listing of various items, including vehicles, phones, computers, and private lessons. This comprehensive platform integrates user authentication, email notifications, and a robust item listing feature to create a seamless user experience.

## Live Site

Check out the live version of Cengden [here](https://cengden-e2gc.onrender.com).

## Features

- **User Authentication**: Secure login and registration functionality powered by Auth0.
- **Dynamic Item Listings**: Users can add, view, and manage listings across various categories.
- **Email Notifications**: Automated email notifications via SendGrid for actions like registration confirmation and item listing updates.
- **Responsive Design**: A mobile-friendly interface that adjusts to different screen sizes for optimal viewing.
- **Admin Dashboard**: Special access for admins to view all users and manage site content.
-**WHEN ADDING LESSONS PLEASE SEPERATE THE LESSON NAMES WITH A COMMA.**: It  splits the comma.
-**IT SEND THE VERIFICATION MAIL BUT I DID NOT IMPLEMENT THE LOGIC IN THE CODE**

## Technology Stack

- **Frontend**: HTML, Bootstrap for styling, and JavaScript for dynamic content manipulation.
- **Backend**: Flask, a Python web framework, to handle server-side logic.
- **Database**: MongoDB for storing user data and item listings.
- **Authentication**: Auth0 for secure user authentication and management.
- **Email Service**: SendGrid for sending out email notifications.
- **Deployment**: Render for hosting and deploying the live application.

## Local Development Setup

### Prerequisites

- Python 3.8+
- MongoDB
- An Auth0 account
- A SendGrid account

### Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/cengden.git
cd cengden
