
from rest_framework.viewsets import ModelViewSet
from rest_access_policy import AccessPolicy

class BankAccessPolicy(AccessPolicy):
  statements = [
    {
      "action": ["list"],
      "principal": ["authenticated"],
      "effect": "allow"
    },
    {
      "action": ["retrieve"],
      "principal": ["group:administrator", "authenticated"],
      "effect": "allow"
    },
    {
      "action": ["destroy"],
      "principal": ["group:administrator"],
      "effect": "allow",
    }
  ]
