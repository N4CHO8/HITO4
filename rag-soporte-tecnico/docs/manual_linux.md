# Manual interno de Linux

## Visualizar procesos

Para visualizar procesos en Linux se recomienda usar `ps aux`, `top` o `htop`.
El comando `ps aux` entrega una lista completa con usuario, PID, uso de CPU,
uso de memoria y comando ejecutado.

Comandos utiles:

```bash
ps aux
top
htop
```

Para buscar un proceso especifico se puede combinar `ps aux` con `grep`:

```bash
ps aux | grep nombre_servicio
```

## Revisar uso de disco

El uso de disco se revisa con `df -h`. Para revisar el peso de directorios se
usa `du -sh ruta`.

## Revisar servicios

En sistemas con systemd se usa `systemctl status nombre_servicio` para revisar
si un servicio esta activo, detenido o fallando.

Si un servicio falla despues de un despliegue, el primer paso es revisar:

1. `systemctl status nombre_servicio`.
2. `journalctl -u nombre_servicio -n 100`.
3. Variables de entorno y permisos de archivos.
4. Conectividad con servicios externos.

