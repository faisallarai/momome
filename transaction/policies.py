
from rest_access_policy import AccessPolicy

class TrannsactionAccessPolicy(AccessPolicy):
  statements = [
    {
      "action": ["list"],
      "principal": ["authenticated"],
      "effect": "allow"
    },
    {
      "action": ["retrieve"],
      "principal": ["group:administrator", "group:executive"],
      "effect": "allow"
    },
    {
      "action": ["create"],
      "principal": ["*"],
      "effect": "allow"
    },
    {
      "action": ["destroy"],
      "principal": ["group:administrator"],
      "effect": "allow",
    }
  ]
