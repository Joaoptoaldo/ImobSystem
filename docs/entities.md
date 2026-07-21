# Diagrama de Entidade-Relacionamento (DER)

[![Diagrama de Entidade-Relacionamento](../diagrams/er-diagram/der.png)](../diagrams/er-diagram/der.png)

Entidades:

- Client
- Immobile
- ImmobileImage
- RegisterLocation

Relacionamentos:

- Client (1) → (N) RegisterLocation
- Immobile (1) → (N) RegisterLocation
- Immobile (1) → (N) ImmobileImage
