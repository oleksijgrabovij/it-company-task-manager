# IT Company Task Manager

A Django-based web application for managing tasks, teams, positions, and worker assignments in an IT company.

## Features
- **User Authentication & Authorization**: Custom `Worker` user model with role-based access control (Staff permissions for admin actions).
- **Task & Worker Management**: Full CRUD capabilities for tasks, positions, task types, and workers.
- **Search & Filtering**: Search workers by name/username and tasks by name and type.
- **Query Optimization**: Efficient database calls using `select_related` and `prefetch_related`.

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/oleksijgrabovij/it-company-task-manager.git
cd it-company-task-manager