from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.author == request.user

class CapexIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.variant.project.author == request.user
