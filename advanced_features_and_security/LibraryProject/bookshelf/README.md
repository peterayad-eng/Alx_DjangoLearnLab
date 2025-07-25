# Permissions & Groups

## Available Permissions

| Permission       | Description          |
|------------------|----------------------|
| `can_view`       | View book listings   |
| `can_create`     | Add new books        |
| `can_edit`       | Modify existing books|
| `can_delete`     | Remove books         |

## User Groups & Access Levels

| Group    | Permissions                          |
|----------|--------------------------------------|
| Viewers  | `can_view`                           |
| Editors  | `can_view`, `can_create`, `can_edit` |
| Admins   | All permissions                      |

## Management Command

To create groups and assign permissions:
```bash
python manage.py setup_groups
```

# Security Measures in LibraryProject

## Settings

- `DEBUG = False`
- `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF` enabled
- `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE` enforce HTTPS-only cookies
- CSP middleware enabled for script/style restrictions

## Forms

- All forms use `{% csrf_token %}` to prevent CSRF attacks

## Views

- All inputs handled via Django Forms and ORM
- No raw SQL queries are used

