"""Role-based access control (RBAC) permissions manager."""

from enum import Enum


class Role(str, Enum):
    """User role levels."""

    ADMIN = "admin"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    VIEWER = "viewer"


ROLE_PERMISSIONS: dict[Role, set[str]] = {
    Role.ADMIN: {"read", "write", "delete", "model_manage", "privacy_audit"},
    Role.OPERATOR: {"read", "write", "stream"},
    Role.DEVELOPER: {"read", "write", "model_train"},
    Role.VIEWER: {"read"},
}


class RBACManager:
    """Manager checking role authorization against required scopes/permissions."""

    @staticmethod
    def has_permission(role: str | Role, required_permission: str) -> bool:
        """Check if role has required permission.

        Args:
            role: User role string or Enum.
            required_permission: Permission string ('read', 'write', 'model_manage').

        Returns:
            True if permission is authorized.
        """
        try:
            role_enum = Role(role)
        except ValueError:
            return False

        allowed = ROLE_PERMISSIONS.get(role_enum, set())
        return required_permission in allowed
