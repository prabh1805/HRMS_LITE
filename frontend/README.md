# HRMS Lite

A production-ready React frontend for an internal HR management system.

## Tech Stack

- React 18 with Vite
- TailwindCSS for styling
- React Router for navigation
- Axios for API calls
- Framer Motion for animations

## Features

- Dashboard with key metrics
- Employee management (add, view, delete)
- Attendance tracking
- Clean enterprise UI design
- Responsive layout
- Loading states and error handling
- Smooth animations and transitions

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

4. Update the `VITE_API_URL` in `.env` to point to your backend API

### Development

Run the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

Create a production build:

```bash
npm run build
```

## Project Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   ├── employee/        # Employee-specific components
│   └── attendance/      # Attendance-specific components
├── pages/               # Page components
├── layout/              # Layout components
├── router/              # Router configuration
├── services/            # API service layer
├── hooks/               # Custom React hooks
└── utils/               # Utility functions and constants
```

## Design System

- Background: `bg-gray-50`
- Cards: `bg-white` with `shadow-sm`
- Primary color: `indigo-600`
- Rounded corners: `rounded-xl`
- Smooth transitions on all interactive elements

## API Integration

The app expects a REST API with the following endpoints:

- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/employees` - List all employees
- `POST /api/employees` - Create new employee
- `DELETE /api/employees/:id` - Delete employee
- `GET /api/attendance` - List attendance records
- `POST /api/attendance` - Mark attendance

Configure the API base URL in the `.env` file.
