from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from .models import Client, Site, Deployment


class SiteSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"

    def validate(self, val):
        if "|" in val["site"]:
            raise ValidationError("Site name cannot contain the | character")

        return val


class ClientSerializer(ModelSerializer):

    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"

    def validate(self, val):

        if "site" in self.context:
            if "|" in self.context["site"]:
                raise ValidationError("Site name cannot contain the | character")
            if len(self.context["site"]) > 255:
                raise ValidationError("Site name too long")

        if "|" in val["client"]:
            raise ValidationError("Client name cannot contain the | character")

        return val


class TreeSerializer(ModelSerializer):
    client_name = ReadOnlyField(source="client.client")

    class Meta:
        model = Site
        fields = (
            "id",
            "site",
            "client_name",
        )


class DeploymentSerializer(ModelSerializer):
    client_id = ReadOnlyField(source="client.id")
    site_id = ReadOnlyField(source="site.id")
    client_name = ReadOnlyField(source="client.client")
    site_name = ReadOnlyField(source="site.site")

    class Meta:
        model = Deployment
        fields = [
            "id",
            "uid",
            "client_id",
            "site_id",
            "client_name",
            "site_name",
            "mon_type",
            "arch",
            "expiry",
            "install_flags",
        ]
