
from rest_framework.viewsets import ModelViewSet
from rest_access_policy import AccessPolicy

class TransferAccessPolicy(AccessPolicy):
  statements = [
    {
      "action": ["list", "retrieve"],
      "principal": ["group:administrator", "group:executive", "authenticated"],
      "effect": "allow"
    },
    {
      "action": ["send", "bulk"],
      "principal": ["group:administrator"],
      "effect": "allow"
    },
    {
      "action": ["destroy"],
      "principal": ["group:administrator"],
      "effect": "allow",
    }
  ]
