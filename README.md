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


## Technology Stack

- **Frontend**: HTML, Bootstrap for styling, and JavaScript for dynamic content manipulation.
- **Backend**: Flask, a Python web framework, to handle server-side logic.
- **Database**: MongoDB for storing user data and item listings.
- **Authentication**: Auth0 for secure user authentication and management.
- **Email Service**: SendGrid for sending out email notifications.
- **Deployment**: Render for hosting and deploying the live application.

- **REASONING BEHIND THESE TECHNOLOGIES**:
Flask: I chose Flask for its simplicity and flexibility. As a micro-framework, Flask provides just the essentials for web development, allowing me to start small and scale up with extensions as needed. It's perfect for rapid development without the overhead of larger frameworks, and its Python base means I can leverage a language I'm already comfortable with. The vast community support for Flask also ensures resources and help are readily available.

HTML: HTML is the backbone of web content. Its universality across web browsers and simplicity make it the ideal choice for structuring the content of the Cengden platform. It allows for seamless integration with CSS for styling and JavaScript for interactive elements, ensuring a rich user experience. The control HTML offers over page structure is crucial for optimizing performance, accessibility, and SEO.

By combining Flask's server-side capabilities with the foundational web structure provided by HTML, I created a scalable, efficient, and user-friendly marketplace platform.

Also Render, Auth0, SendGrid and MongoDB has native suport for Flask and it has made the implementation process much more easier.



## Login Information
- **ADMIN USER INFO**: Username: mertsagcan99@gmail.com    Password: ceng495CLOUD
- **REGULAR USER INFO**: Username: 2310449@ceng.metu.edu.tr  Password: 123qwe123QWE

- **IT SENDS THE VERIFICATION MAIL BUT I DID NOT IMPLEMENT THE LOGIC IN THE CODE**

- **WHEN ADDING LESSONS PLEASE SEPERATE THE LESSON NAMES WITH A COMMA.**: It  splits the comma.






