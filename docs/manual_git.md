# Manual interno de Git

## Actualizar un repositorio

Para actualizar un repositorio Git local se debe confirmar primero la rama
actual con `git branch` o `git status`. Luego se ejecuta `git pull` para traer
los ultimos cambios del remoto configurado.

Procedimiento recomendado:

1. Ejecutar `git status`.
2. Guardar o confirmar cambios locales antes de actualizar.
3. Ejecutar `git pull origin nombre-rama`.
4. Resolver conflictos si Git los informa.
5. Ejecutar pruebas antes de desplegar.

Si existen cambios locales no confirmados, se puede usar `git stash` antes del
pull y luego `git stash pop`, siempre revisando los archivos modificados.

## Crear una rama

Las ramas nuevas se crean con:

```bash
git checkout -b nombre-rama
```

## Registrar cambios

Para registrar cambios se usa `git add` y `git commit`:

```bash
git add archivo
git commit -m "descripcion breve"
```

