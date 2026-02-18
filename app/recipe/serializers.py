"""
Serializer for recipe APIs.
"""

from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects."""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a recipe."""
        tags_data = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context["request"].user
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                user=auth_user, **tag_data
            )
            recipe.tags.add(tag)
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]

    def validate(self, attrs):
        """Validate the serializer data."""
        if "user" in self.initial_data:
            raise serializers.ValidationError("User cannot be updated.")
        return attrs


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]
