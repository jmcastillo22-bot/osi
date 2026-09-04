# Plan de ejecución · Nueva estructura web de La Casa de Hormigón

**Cliente:** CVH PRECAST S.L. · **Prestador:** OSI Global Consulting SL
**Fase:** F3 · Marca con garantía y página profesional
**Base:** propuesta «Nueva estructura web» — Opción A · Doble puerta (Profesionales / Particulares), Club en WordPress por fases (`propuestawebcvh.pdf`, enviado por correo)
**Fecha del documento:** 04/09/2026 · **Gate de aprobación:** 08/09/2026 · **Publicación:** 11/09/2026

---

## 1. Causa raíz de por qué el plan no está cerrado

No es un problema de diseño ni de contenidos: es un **gate de aprobación vencido**.

| Hecho | Evidencia |
|---|---|
| La aprobación de estructura y contenidos tenía fecha objetivo **28/08** y sigue en *En curso* | Plan de Acción · «Página profesional: estructura y contenidos + APROBACIÓN del interlocutor (dependencia crítica)» |
| El riesgo ya estaba registrado y sigue **Abierto** | Riesgos & Issues · «Aprobación de la página profesional retrasada (S6)», impacto Medio, responsable Cliente · interlocutor |
| Faltan tres insumos del cliente sin los que no se puede redactar | Evidencia de la tarea (18/08): **3 obras con plazo y coste**, **fotos**, **plugin de formularios** |
| La publicación del 11/09 depende de esa aprobación | Plan de Acción · «Publicación de la página profesional + redacción de casos con datos y argumentario», 11/09, Alta |

Sin decisión formal de arquitectura no se puede repartir la redacción, y sin redacción repartida no hay publicación el 11/09. **Todo el plan cuelga de los 90 minutos del día 8.**

---

## 2. Restricción de calendario: el 11/09 no admite el alcance completo

Del 08/09 (fin de la reunión, 11:30) al 11/09 (publicación) hay **2 días hábiles: miércoles 9 y jueves 10**. En esa ventana caben:

- la actualización de los 13 plugins con prueba previa en staging,
- la redacción y maquetación de los bloques repartidos,
- el mapa de redirecciones y la revisión de medición,
- el ensayo de publicación.

No caben, además, los contenidos que dependen de datos que el cliente todavía no ha entregado. **Hay que cortar el alcance en la reunión, no después.**

### Corte propuesto (llevar decidido como opción por defecto)

| Se publica el 11/09 (MVP) | Va a fase 2 (semanas del 15 y 22/09) |
|---|---|
| Bifurcación de entrada Profesional / Particular con conmutador permanente | Club de La Casa de Hormigón (ya acordado fuera de alcance el 17/08, punto 9) |
| Página profesional B2B completa: 4 perfiles del canal + formulario bifurcado con SLA <5 min | Rangos €/m² del recorrido particular (requieren validación comercial) |
| 2–3 casos de obra **solo con los datos que Javier confirme el día 8** | Catálogo B2B completo con ficha por producto |
| Recuperación del catálogo B2B en su versión mínima y reapuntado de las 3 redirecciones provisionales de `/colaboracion-con-profesionales/` | Calendario editorial (ya planificado al 25/09) |

Publicar el MVP el 11/09 **cierra el riesgo de mayor probabilidad del programa** (*«El catálogo de producto B2B no tiene página viva y depende de un tercero»*, impacto Alto / probabilidad Alta), que la propia mitigación fecha en la publicación del 11/09.

---

## 3. Las ocho decisiones que deben salir cerradas del día 8

Cada una con opción por defecto, para que la reunión decida y no delibere.

| # | Decisión | Opción por defecto de OSI | Si no se cierra |
|---|---|---|---|
| 1 | Alcance del 11/09 | MVP de la tabla anterior; el resto en dos fases | Se mueve la publicación |
| 2 | Árbol de URLs y canónicas de la Opción A | URLs nuevas bajo la ruta profesional; `/colaboracion-con-profesionales/` reapuntada al destino definitivo el mismo 11/09 | Se arrastran redirecciones provisionales y cadenas de saltos |
| 3 | Casos de obra publicables | Bonanza, vivienda piloto de Valdemorillo y estructuras para promotoras, con plazo y superficie; coste en **rango**, no en cifra cerrada | Los bloques de prueba social se publican vacíos |
| 4 | Plugin de formularios y campos | El que ya use producción; campos alineados con la taxonomía de perfiles + «¿cómo nos ha conocido?» + ORIGEN | El lead entra sin ORIGEN y no computa limpio para C1 |
| 5 | Club LCH | Fuera del 11/09, documento y presupuesto aparte | Deriva de alcance hacia proyecto técnico no vendido (riesgo ya en vigilancia) |
| 6 | Futuro de la caché | Sustituir por caché de servidor en Plesk hasta que WP Rocket publique versión corregida y probada en staging | Se publica una estructura nueva sobre un sitio sin caché |
| 7 | Reparto de redacción por bloques | Matriz del apartado 5, entrega **09/09 a las 20:00** | No hay material que maquetar el día 10 |
| 8 | Quién firma el go/no-go del 11/09 y a qué hora | Javier (CVH) + OSI senior, **10/09 a las 18:00**, sobre la checklist del apartado 7 | Se publica sin criterio de parada |

---

## 4. Bloqueantes técnicos que hay que resolver antes de publicar

### 4.1 Base WordPress (bloque de las 09:00)

Origen: la incidencia del **20–24/08**, en la que un error fatal de WP Rocket 3.20.0.3 dejó la web sin login, sin formularios y sin páginas no cacheadas **durante 4 días sin que nadie lo detectara**.

| Punto | Estado | Acción antes del 11/09 |
|---|---|---|
| 13 plugins con actualización pendiente | Sin aplicar | Probar en staging y aplicar a producción con copia previa y registro de cambios |
| Actualizaciones automáticas | Desactivadas en los 20 plugins | Política: automáticas en seguridad, con prueba previa en Elementor y ecosistema de maquetación |
| Caché | WP Rocket desactivado desde el 24/08 | Decisión 6 |
| Aviso de administrador de WordPress | A buzón no vigilado | Redirigir a buzón vigilado — es lo que convirtió una caída en 4 días de caída |
| Copias de seguridad | Diarias desde el 24/08 (BD + archivos, retención 2) | Verificar la copia de la noche previa antes de tocar producción |

**La ventana de trabajo propuesta era «semana del 01–08/09, fuera de horario comercial».** A día de hoy queda solo la noche del **8 al 9**. Hay que confirmarla en la reunión de las 09:00 o el margen desaparece.

### 4.2 Medición — bloqueante para el bonus del Anexo II

El sitio mide con el contenedor **GTM-W2X6WWKZ, que no controla ni CVH ni OSI** (hallazgo abierto desde el 17/08). Si la nueva estructura se publica sin resolverlo, los eventos del formulario profesional pueden quedar sin trazar, y **C1 se mide sobre el registro comercial, no sobre la web**: el riesgo no es perder el bonus, es perder la capacidad de explicar de dónde vino cada lead.

Acción: reclamar el acceso al contenedor o desplegar contenedor propio **antes** de publicar, y tomar la línea base de la web el **10/09**, con la estructura vieja todavía en producción.

### 4.3 Deuda de indexación que se arrastraría a la web nueva

| Incidencia | Desde | Corrección |
|---|---|---|
| Complianz sirve `/wp-content/uploads/complianz/css/banner-{banner_id}-{type}.css?v=18` con los marcadores literales sin sustituir | 28/06/2026 | No se arregla con redirección: hay que actualizar o revisar la configuración del plugin |
| Slug con emoji `/🏡-tendencias-de-mobiliario-.../` que Google no reconoce | — | Cambiar slug + redirección, agrupado en la misma ventana |
| 3 imágenes de `/wp-content/uploads/` en 404 que llegaron a tener impresiones | — | Revisión de medios |

Las tres entran en la ventana del 8 al 9. Publicar encima sin corregirlas mantiene los errores en la cobertura de Search Console justo cuando se empieza a medir la estructura nueva.

---

## 5. Reparto de redacción por bloques

La estructura v1 (redactada el 14/08, `Pagina_Profesional_B2B_Estructura_v1_OSI_lacasadehormigon.docx`) tiene **8 bloques, 4 perfiles del canal profesional, 3 casos de obra citables y formulario bifurcado**. La matriz se rellena en la reunión contra ese documento; el criterio de reparto es el siguiente:

| Tipo de bloque | Redacta | Motivo | Entrega |
|---|---|---|---|
| Argumentario técnico, certificaciones DIT/ETE, especificaciones | **Javier (CVH)** | Es dato de producto, no se puede escribir desde fuera | 09/09 20:00 |
| Datos de las 3 obras (plazo, superficie, rango de coste, fotos) | **Javier (CVH)** | Dependencia crítica ya identificada desde el 18/08 | 09/09 20:00 |
| Los 4 perfiles del canal profesional y su propuesta de valor | **OSI** | Sale del Perfil de Cliente Objetivo v2 | 09/09 20:00 |
| Bloques de conversión: formulario, preacuerdo, SLA <5 min, WhatsApp centralizado | **OSI** | Ya validados en la sesión del 20/08 | 09/09 20:00 |
| Textos legales, avisos y cookies | **OSI** | Ligado a Complianz | 10/09 12:00 |
| Maquetación e integración de todo | **OSI operación** | — | 10/09 18:00 |

**Regla que conviene dejar dicha en la reunión:** lo que no esté entregado el **09/09 a las 20:00** no entra en la publicación del 11/09; se publica el bloque con la versión de OSI o se deja fuera. Sin esa regla, el día 10 se convierte en negociación en vez de en maquetación.

---

## 6. Cronograma D-3 → D+7

| Fecha | Hora | Quién | Acción |
|---|---|---|---|
| 08/09 | 09:00–09:30 | OSI → Cliente | Presentar propuesta de mantenimiento; confirmar ventana nocturna 8→9 |
| 08/09 | 10:00–11:30 | Ambos | Cerrar las 8 decisiones + reparto de bloques |
| 08/09 | mismo día | OSI | Enviar acta con acuerdos y deberes, por escrito |
| 08→09/09 | noche | OSI operación | Copia previa · 13 plugins en staging → producción · Complianz · slug emoji · imágenes 404 · admin_email |
| 09/09 | mañana | OSI | Verificación post-actualización: login, formularios, páginas no cacheadas, checkout de canales |
| 09/09 | 20:00 | Javier + OSI | **Tope de entrega de textos y datos de obra** |
| 10/09 | 09:00–18:00 | OSI operación | Maquetación, mapa de redirecciones, revisión de medición |
| 10/09 | 18:00 | Javier + OSI senior | **Go / No-Go** sobre la checklist del apartado 7 |
| 10/09 | 18:00 | OSI | Línea base de medición con la estructura vieja aún en producción |
| 11/09 | fuera de horario | OSI operación | Copia previa → publicación → reapuntado de las 3 redirecciones provisionales → registro de cambios |
| 11/09 | +2 h | OSI | Verificación en producción y solicitud de indexación en Search Console |
| 12–18/09 | — | OSI | Vigilancia de cobertura, rendimiento y primeros leads del formulario |

---

## 7. Checklist Go / No-Go del 10/09 a las 18:00

Publicación **solo** si las nueve líneas están en verde:

1. Copia de seguridad de la noche previa verificada y restaurable.
2. Los 13 plugins actualizados en producción, con login, formularios y páginas no cacheadas comprobados.
3. Complianz corregido: la ruta del CSS resuelve y devuelve 200.
4. Mapa de redirecciones cerrado, sin cadenas de más de un salto y sin destinos a portada.
5. Formulario profesional enviando al buzón correcto, con «¿cómo nos ha conocido?» y ORIGEN, probado extremo a extremo.
6. Medición: contenedor GTM resuelto o contenedor propio desplegado y disparando el evento de envío.
7. Textos y datos de obra entregados y maquetados; ningún bloque con marcador ámbar de dato pendiente.
8. Rendimiento aceptable sin WP Rocket (o con la caché sustituta ya activa) en la página profesional en móvil.
9. Registro de cambios abierto y aviso de administrador apuntando a buzón vigilado.

Si falla cualquiera de la 1 a la 6, **no se publica**: se mueve al 15/09. Si falla la 7, se publica el MVP recortado.

---

## 8. KPIs

### Contractuales (no cambian con esta publicación)
- **C1 frente a C0 = 0,8 %** sellada en el acta firmada el 18/08, medida sobre el **total del registro** (Anexo II v3, firmado el 24/08).
- Mínimo de **25 presupuestos** en la ventana de medición final (estimación actual ~42).
- Tres actas de hito aceptadas.

### Operativos del protocolo (ya en uso)
- Tiempo de primera respuesta **< 5 min**.
- % de leads con **ORIGEN** informado en CRM — hoy bloqueado por el partner de Odoo, sin plazo comprometido.
- % de oportunidades con motivo de pérdida a 14 días.

### De la web (nuevos — línea base a tomar el **10/09**, antes de publicar)
| Indicador | Medición | Objetivo a 30 días |
|---|---|---|
| Leads del formulario profesional | Semanal | Tendencia al alza sobre la línea base del 10/09 |
| Tasa de envío del formulario | Visitas a la página profesional → envíos | Establecer línea base y mejorarla |
| Páginas de la estructura nueva indexadas | Search Console, a 7 y 14 días | 100 % de las URLs publicadas |
| Errores de cobertura | Search Console | 0 errores **nuevos** atribuibles a la publicación |
| LCP en móvil de la página profesional | Antes / después | No degradar respecto al 10/09 |
| URLs en 404 tras la publicación | Registro de cambios | 0 |

---

## 9. Quick wins (coste bajo, efecto inmediato)

1. **Aviso de administrador a buzón vigilado.** Cinco minutos. Es lo único que separa una incidencia de una caída de cuatro días sin detectar.
2. **Complianz.** Cierra un 404 abierto desde el 28/06 que se lleva arrastrando en cobertura.
3. **Slug con emoji + su redirección.** Una URL que Google no reconoce, agrupada en la misma ventana para no encadenar redirecciones sueltas.
4. **Tres imágenes en 404** que llegaron a tener impresiones.
5. **Reapuntar las 3 redirecciones provisionales** de `/colaboracion-con-profesionales/` el mismo 11/09, aprovechando que la página destino ya existe.
6. **Reclamar el contenedor GTM** por escrito el día 8: es gratis, y sin él la medición de la web nueva nace ciega.

---

## 10. Impacto en integraciones

| Integración | Efecto de la publicación | Qué vigilar |
|---|---|---|
| **Search Console** | URLs nuevas + redirecciones reapuntadas | Cobertura a 7 y 14 días; que el dominio canónico siga siendo el `.es` |
| **GA4** | Cambio de estructura de rutas | Que los informes por página no se rompan; anotar la fecha de publicación |
| **GTM-W2X6WWKZ** | Contenedor ajeno | Bloqueante: resolver antes de publicar |
| **Odoo / crm.lead** | El formulario nuevo alimenta el CRM | Campos perfil, importe y ORIGEN siguen pendientes del partner del cliente, sin plazo |
| **Complianz** | Consentimiento y textos legales | Que la corrección del CSS no altere el banner |
| **WhatsApp centralizado** | Ya en producción desde el 26/08 | Prueba extremo a extremo tras actualizar plugins |
| **Plesk / caché** | Sustituta de WP Rocket | Purgado tras publicar, o se sirve la estructura vieja |
