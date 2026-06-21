# Implementación de un Analizador Léxico, Sintáctico y Semántico en C#
> **Safe C# Linter** — Validador de código para transacciones financieras

## Miembros
 
- Victor Morales
- José Adrian
- Andres Saltos
## Avance 1 - Analizado Léxico

### Treas a realizar
- Agregar sus tokens en el archivo `lexer.py` con comentario de inicio y fin
- Crear el algoritmo de prueba siguiendo las instrucciones de la tarea `algoritmo1.cs` lo ideal es que el número que acampaña a algoritmo vaya en sucesión según el orden de los integrantes :D
- Ejecutar el analizador y que se guarde en la carpeta `/logs/`

### Convención de issues

Los issues deben tener el formato: `[tipo] descripción corta del problema`

| Tipo | Uso |
|------|-----|
| `[bug]` | Algo no funciona correctamente |
| `[enhancement]` | Mejora o cobertura faltante en algo que ya funciona |
| `[docs]` | Documentación incompleta o incorrecta |
| `[question]` | Duda o consulta sobre el proyecto |

Ejemplos:
- `[bug] lexer no reconoce operador !=`
- `[enhancement] list_decl no es accesible desde stmt_list`
- `[docs] README sin instrucciones de ejecución del parser`

### Convención de ramas

Las ramas deben seguir el formato: `tipo/descripcion-corta`

| Tipo | Uso |
|------|-----|
| `feature` | Nueva funcionalidad o aporte |
| `fix` | Corrección de un error |
| `docs` | Cambios en documentación |
| `refactor` | Mejora de código sin cambiar funcionalidad |

Ejemplos:
- `feature/lexer-victor`
- `fix/parser-list-decl`
- `docs/readme-convenciones`

### Convención de commits

Para que tengamos un orden usaremos tipos:

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad o aporte |
| `fix` | Corrección de un error |
| `docs` | Cambios en documentación |
| `refactor` | Mejora de código sin cambiar funcionalidad |
| `test` | Agregar o modificar pruebas |

# Ejecución de su algoritmo.cs
`python src/lexer.py algoritmos/algoritmo[Número correspondiente].cs`