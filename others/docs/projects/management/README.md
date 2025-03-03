# Team Management Application

## Overview
Team Management is a web-based application built with Nuxt.js for managing team activities, timesheets, and projects. It provides a comprehensive solution for tracking work hours, managing projects, and generating reports.

## Features

### Authentication System
- Secure login system with role-based access control (Admin/User)
- Persistent authentication using localStorage
- Protected routes and API endpoints
- Session management with auto-logout functionality

### User Roles
1. **Admin Users**
   - Full access to all features
   - Project management capabilities
   - Access to admin dashboard
   - User management
   - Report generation

2. **Regular Users**
   - Timesheet management
   - Personal dashboard access
   - View assigned projects
   - Generate personal reports

### Dashboard
- Quick overview of key metrics:
  - Today's work hours
  - Weekly total hours
  - Active tasks count
  - Monthly hours summary
- Recent timesheet entries
- Quick access to frequent actions
- Project status overview

### Timesheet Management
1. **Entry Creation**
   - Date selection with date picker
   - Project selection from available projects
   - Task description
   - Regular hours tracking (0-12 hours) with slider
   - Overtime hours tracking (0-8 hours) with slider
   - Start/End time selection
   - Status tracking (Pending/In Progress/Completed)

2. **Entry Management**
   - Edit existing entries
   - Delete entries
   - View entry history
   - Status updates

### Project Management (Admin Only)
1. **Project Creation**
   - Project name
   - Description
   - Creation date tracking
   - Last update tracking

2. **Project Operations**
   - Create new projects
   - Edit existing projects
   - Delete projects
   - View project details
   - Track project status

### Reports
1. **Summary Statistics**
   - Total hours worked
   - Project-wise distribution
   - Overtime analysis
   - Task completion rates

2. **Visualizations**
   - Hours by project (Bar Chart)
   - Daily hours distribution (Line Chart)
   - Project progress tracking
   - Time utilization metrics

### Navigation
1. **Desktop View**
   - Sidebar navigation with:
     - Dashboard
     - Timesheet
     - Projects (Admin)
     - Reports
     - User profile
     - Logout option

2. **Mobile View**
   - Bottom navigation bar
   - Responsive design
   - Touch-friendly interface
   - Collapsible menus
