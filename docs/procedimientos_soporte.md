# Procedimientos internos de soporte

## Apertura de ticket

Todo incidente debe registrarse como ticket antes de iniciar la atencion. El
ticket debe incluir:

- Nombre del usuario afectado.
- Servicio o aplicacion comprometida.
- Descripcion del problema.
- Hora de inicio.
- Evidencia disponible, como capturas, logs o mensajes de error.
- Nivel de prioridad.

La prioridad alta se usa cuando existe indisponibilidad total, perdida de datos
o impacto en multiples usuarios.

## Diagnostico inicial

El tecnico debe reproducir el problema o solicitar evidencia. Luego debe revisar
logs, conectividad, estado de servicios y cambios recientes. Si el problema
ocurrio despues de un despliegue, se debe comparar la version actual con la
version anterior y ejecutar pruebas de humo.

## Escalamiento

Un ticket se escala cuando supera 30 minutos sin diagnostico claro, afecta a
mas de un area o requiere permisos que el tecnico no posee.

## Cierre de ticket

Para cerrar un ticket se debe registrar la causa raiz, la solucion aplicada,
la evidencia de validacion y las recomendaciones para evitar recurrencia.

