# Booking Ticket

If you’d like to simplify this project by removing the payment functionality, here’s how the README would look:

---

# Booking Ticket

This project is a **Ticket Booking Application** designed for managing ticket reservations for events, shows, or travel (like flights and trains). It provides users with options to search, book, and manage their bookings through an API-driven interface.

## Project Overview

The Ticket Booking App is a RESTful API service that allows users to:
- View available events or travel schedules
- Book tickets
- Manage their bookings (update or cancel)

The project supports different user roles (e.g., User, Admin) with distinct permissions for accessing and managing tickets and events.

---

## Features

### 1. User Management
- **User Registration**: Users can register with their name, email, and password.
- **User Login**: Registered users can log in to access their profile and bookings.
- **User Profile**: Users can view and update their profile information.
- **Password Reset**: Users can reset their passwords.

### 2. Event/Travel Management (Admin)
- **Add Event/Travel Schedule**: Admins can create new events or travel schedules, specifying details like date, time, venue, and seat availability.
- **Update Event/Travel Schedule**: Admins can modify the details of events or schedules.
- **Delete Event/Travel Schedule**: Admins can remove events that are no longer available.

### 3. Booking Management
- **View Available Events/Schedules**: Users can browse events or travel schedules and view details.
- **Book Ticket**: Users can book tickets for available events/schedules.
- **View Bookings**: Users can see a list of their booked tickets.
- **Cancel Booking**: Users can cancel a booking before the event date.
- **Download/Receive Ticket Confirmation**: Users receive a booking confirmation with details (PDF/email).

### 4. Notifications
- **Booking Confirmation**: Users receive a notification or email with booking confirmation details.
- **Reminders**: Users receive a reminder before the event date.

---

## API Documentation

This API provides endpoints to handle user registration, login, event management, and booking.

### Authentication & Authorization
Some routes are protected and require an authentication token.

**Endpoints**:

- **POST** `/auth/register` – Register a new user.
- **POST** `/auth/login` – Log in an existing user.
- **POST** `/auth/logout` – Log out the user.

### User Routes

- **GET** `/user/profile` – Retrieve the user's profile.
- **PUT** `/user/profile` – Update user profile information.
- **POST** `/user/reset-password` – Send a password reset link.

### Event/Travel Routes (Admin Only)

- **POST** `/admin/event` – Create a new event/travel schedule.
  - **Parameters**: `name`, `date`, `time`, `venue`, `seat_count`
- **PUT** `/admin/event/{event_id}` – Update an existing event/travel schedule.
- **DELETE** `/admin/event/{event_id}` – Delete an event/travel schedule.
- **GET** `/admin/events` – View all events.

### Booking Routes

- **GET** `/events` – View available events/travel schedules.
- **POST** `/booking` – Book a ticket for an event.
  - **Parameters**: `event_id`, `user_id`, `seat_type`
- **GET** `/booking/{booking_id}` – View a specific booking.
- **GET** `/user/bookings` – View all bookings for the authenticated user.
- **DELETE** `/booking/{booking_id}` – Cancel a booking.

### Notification Routes

- **GET** `/notifications` – View all notifications for the user.
- **POST** `/notifications/send` – Send a booking confirmation notification (auto-triggered after booking).
