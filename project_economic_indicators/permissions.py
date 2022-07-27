from rest_framework import permissions


class IsOwnerCapex(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user

class IsOwnerFile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.object.project.author == request.user
