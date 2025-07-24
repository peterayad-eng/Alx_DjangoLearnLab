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

