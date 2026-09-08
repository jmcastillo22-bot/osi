#!/usr/bin/env python3
"""Genera los documentos presentables de CVH con el membrete estándar de OSI.

Reutiliza el armazón del informe fiscal ya entregado al cliente
(informes/informe_fiscal_osi_v2.html): estilos, paleta, tipografía y membrete
con el logotipo incrustado. Así la marca es idéntica byte a byte y no depende
de volver a pegar el logotipo en cada documento.
"""

import pathlib
import re
import shutil
import subprocess

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / "informes" / "informe_fiscal_osi_v2.html"
SALIDA = RAIZ / "informes"

CORTE = '\n  <header class="title">'

# El informe original se sirvió como fragmento. Estos documentos se abren y se
# imprimen sueltos, así que necesitan cabecera propia y márgenes de página.
IMPRESION = """<style>
  @page{size:A4;margin:16mm 14mm}
  @media print{.tiles{break-inside:avoid} table{break-inside:auto} tr{break-inside:avoid}}
</style>"""


def armazon(titulo):
    """Devuelve la cabecera del documento: estilos + membrete con logotipo."""
    fuente = PLANTILLA.read_text(encoding="utf-8")
    if CORTE not in fuente or "</style>" not in fuente:
        raise SystemExit(f"No se encuentra el membrete en {PLANTILLA}")
    estilos, resto = fuente.split("</style>", 1)
    estilos = re.sub(r"<title>.*?</title>", f"<title>{titulo}</title>", estilos, count=1)
    membrete = resto.split(CORTE)[0]
    return (
        "<!doctype html>\n<html lang=\"es\">\n<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"{estilos}</style>\n{IMPRESION}\n</head>\n<body>{membrete}"
    )


def documento(titulo, subtitulo, meta, cuerpo, pie_derecho):
    return f"""{armazon(titulo)}
  <header class="title">
    <h1>{titulo}</h1>
    <p class="sub">{subtitulo}</p>
    <p class="meta">{meta}</p>
  </header>
{cuerpo}
  <footer>
    <span>OSI Global Consulting, S.L. &middot; NIF B-22831267 &middot; C/ Francisco Alonso 2, Of. 13 &middot; 28660 Boadilla del Monte &middot; info@osigc.es</span>
    <span>{pie_derecho}</span>
  </footer>
</div>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Documento 1 · Propuesta de mantenimiento web (bloque de las 09:00)
# --------------------------------------------------------------------------

MANTENIMIENTO = """
  <div class="tiles">
    <div class="tile"><div class="n">4 días</div><div class="l">sin acceso de administración, formularios ni páginas no cacheadas (20&ndash;24/08)</div></div>
    <div class="tile"><div class="n">13 / 20</div><div class="l">plugins con actualización pendiente</div></div>
    <div class="tile"><div class="n">29/07</div><div class="l">última copia de seguridad antes de la incidencia</div></div>
    <div class="tile"><div class="n">1 noche</div><div class="l">de ventana disponible antes de la publicación del 11/09</div></div>
  </div>

  <h2>1. Por qué esta propuesta</h2>
  <p class="lede">Del <b>20 al 24 de agosto</b> la web estuvo sin acceso de administración, sin formularios y sin las páginas que no estaban en caché. La causa fue un error fatal de la versión <b>3.20.0.3 del plugin WP&nbsp;Rocket</b> en su integración con Cloudflare. El servicio se restauró el 24/08.</p>
  <p>La incidencia no duró cuatro días por su gravedad técnica: se resolvió en cuanto se identificó el plugin culpable. Duró cuatro días porque <b>el aviso de administrador de WordPress llega a un buzón que nadie revisa</b>. Ese es el punto que conviene corregir primero, y es el más barato de los cuatro que se proponen.</p>

  <h2>2. Situación encontrada el 24/08</h2>
  <div class="tw"><table>
    <thead><tr><th>Punto</th><th>Estado</th><th>Consecuencia</th></tr></thead>
    <tbody>
      <tr><td class="k">Plugins</td><td>20 instalados, <b>13 con actualización pendiente</b></td><td>Superficie de fallo y de seguridad creciente</td></tr>
      <tr><td class="k">Actualizaciones automáticas</td><td>Desactivadas en los 20</td><td>Ningún parche de seguridad entra solo</td></tr>
      <tr><td class="k">Copias de seguridad</td><td>Sin programar; la última era del 29/07</td><td>26 días sin punto de restauración</td></tr>
      <tr><td class="k">Caché de página</td><td>WP Rocket desactivado para restaurar el servicio</td><td>La web funciona con normalidad, pero más lenta</td></tr>
      <tr><td class="k">Aviso de administrador</td><td>Dirigido a un buzón no vigilado</td><td>Convirtió una incidencia en cuatro días de caída</td></tr>
    </tbody>
  </table></div>

  <h2>3. Lo que ya está resuelto</h2>
  <p>Sin coste añadido y sin decisión pendiente por su parte:</p>
  <ul class="dash">
    <li><span class="chip ok">Hecho</span> Servicio restaurado el 24/08.</li>
    <li><span class="chip ok">Hecho</span> Copia de seguridad completa lanzada ese mismo día.</li>
    <li><span class="chip ok">Hecho</span> Programación de copias <b>diarias</b> en marcha: base de datos y archivos, con retención 2.</li>
  </ul>

  <h2>4. Lo que proponemos</h2>
  <div class="tw"><table>
    <thead><tr><th class="num">#</th><th>Acción</th><th>Cómo se ejecuta</th><th>Cuándo</th></tr></thead>
    <tbody>
      <tr><td class="num">1</td><td class="k">Actualizar los 13 plugins pendientes</td><td>Prueba previa en el entorno de pruebas; aplicación a producción con copia previa y anotación en el registro de cambios</td><td>Antes del 11/09</td></tr>
      <tr><td class="num">2</td><td class="k">Definir la política de mantenimiento</td><td>Actualización automática en los plugins de seguridad; actualización con prueba previa en los críticos de maquetación (Elementor y su ecosistema)</td><td>Decisión del 08/09</td></tr>
      <tr><td class="num">3</td><td class="k">Decidir el futuro de la caché</td><td>Reactivar WP Rocket solo cuando publique una versión corregida y probada, o sustituirlo</td><td>Decisión del 08/09</td></tr>
      <tr><td class="num">4</td><td class="k">Trasladar el aviso de administrador a un buzón vigilado</td><td>Cambio de la dirección de notificaciones de WordPress</td><td>Misma ventana</td></tr>
    </tbody>
  </table></div>

  <div class="note">
    <p><b>Recomendación de OSI sobre la caché.</b> Sustituirla mientras tanto por la caché de servidor de Plesk. Publicar la nueva estructura web sobre un sitio sin caché alguna degrada precisamente las páginas que se van a empezar a medir.</p>
  </div>

  <h2>5. Se incluyen en la misma ventana</h2>
  <p>Tres correcciones detectadas en el diagnóstico de indexación del 26/08. Ninguna justifica tocar producción por separado, y las tres conviene resolverlas antes de publicar la estructura nueva.</p>
  <div class="tw"><table>
    <thead><tr><th>Incidencia</th><th>Abierta desde</th><th>Corrección</th></tr></thead>
    <tbody>
      <tr><td>El plugin <b>Complianz</b> publica una ruta de hoja de estilos con los marcadores de plantilla sin sustituir, de modo que la petición no encuentra fichero</td><td class="src">28/06/2026</td><td>No se corrige con una redirección: hay que actualizar o revisar la configuración del plugin</td></tr>
      <tr><td>Una <b>URL con emoji en el slug</b> que el buscador no reconoce</td><td class="src">&mdash;</td><td>Cambio de slug y su redirección, agrupado aquí para no encadenar redirecciones sueltas</td></tr>
      <tr><td><b>Tres imágenes</b> de la biblioteca de medios que devuelven error 404 y llegaron a tener impresiones</td><td class="src">&mdash;</td><td>Entran en la revisión de medios</td></tr>
    </tbody>
  </table></div>

  <h2>6. Ventana de trabajo y condiciones</h2>
  <p>La ventana propuesta era la semana del <b>1 al 8 de septiembre</b>, fuera de horario comercial. A fecha de hoy queda disponible la <b>noche del 8 al 9</b>. La verificación posterior &mdash;acceso de administración, formularios, páginas no cacheadas y prueba extremo a extremo de canales&mdash; se hace la mañana del 9.</p>
  <ul class="dash">
    <li>Ningún cambio sin copia de seguridad previa y sin anotación en el registro de cambios. Es una regla fija del programa.</li>
    <li>La copia de la noche anterior se verifica antes de tocar producción.</li>
    <li>Si algo falla, la restauración se hace desde esa copia sin esperar a diagnóstico.</li>
  </ul>

  <h2>7. Qué pedimos aprobar el 8 de septiembre</h2>
  <div class="tw"><table>
    <thead><tr><th>Decisión</th><th>Opción por defecto</th><th>Aprobada</th></tr></thead>
    <tbody>
      <tr><td class="k">Ventana de mantenimiento</td><td>Noche del 8 al 9 de septiembre, fuera de horario comercial</td><td class="src">&#9744;</td></tr>
      <tr><td class="k">Política de actualizaciones</td><td>Automáticas en seguridad, con prueba previa en maquetación</td><td class="src">&#9744;</td></tr>
      <tr><td class="k">Futuro de la caché</td><td>Sustituir por caché de servidor en Plesk</td><td class="src">&#9744;</td></tr>
      <tr><td class="k">Buzón vigilado</td><td>Dirección concreta a la que se trasladan los avisos</td><td class="src">&#9744;</td></tr>
    </tbody>
  </table></div>

  <div class="note caution">
    <p><b>Si no se aprueba.</b> La nueva estructura web se publicaría el 11/09 sobre 13 plugins sin actualizar, sin caché y con los errores de indexación todavía abiertos, justo cuando se empieza a medir el rendimiento de esa estructura.</p>
  </div>

  <p class="small">Evidencia técnica disponible a petición: informe de diagnóstico de indexación del 26/08/2026 y listas de cobertura descargadas de Search Console, archivadas con huella. Programa de Crecimiento B2B &middot; Fase 3 &middot; Marca con garantía y página profesional.</p>
"""


# --------------------------------------------------------------------------
# Documento 2 · Plan de ejecución de la nueva estructura web (bloque 10:00)
# --------------------------------------------------------------------------

PLAN = """
  <div class="tiles">
    <div class="tile"><div class="n">2 días</div><div class="l">hábiles entre el cierre de la sesión y la publicación</div></div>
    <div class="tile"><div class="n">8</div><div class="l">decisiones que deben salir cerradas el 08/09</div></div>
    <div class="tile"><div class="n">7 días</div><div class="l">de retraso sobre la aprobación prevista para el 28/08</div></div>
    <div class="tile"><div class="n">3</div><div class="l">insumos del cliente pendientes desde el 18/08</div></div>
  </div>

  <div class="legend">
    <span><span class="chip ok">Listo</span> disponible y verificado</span>
    <span><span class="chip warn">Pendiente</span> depende de una decisión o de un insumo del cliente</span>
    <span><span class="chip bad">Bloqueante</span> impide publicar si no se resuelve</span>
  </div>

  <h2>1. Causa raíz: un gate de aprobación vencido</h2>
  <p class="lede">El plan no está cerrado por un motivo concreto, y no es de diseño ni de contenidos. La tarea <b>&laquo;Página profesional: estructura y contenidos + aprobación del interlocutor&raquo;</b> tenía fecha objetivo el <b>28/08</b> y sigue en curso. Sin decisión formal de arquitectura no se puede repartir la redacción, y sin redacción repartida no hay publicación el 11/09.</p>
  <div class="tw"><table>
    <thead><tr><th>Hecho</th><th>Estado</th><th>Origen</th></tr></thead>
    <tbody>
      <tr><td>Aprobación de estructura y contenidos</td><td><span class="chip bad">Bloqueante</span> vencida el 28/08, en curso</td><td class="src">Plan de Acción, dependencia crítica</td></tr>
      <tr><td>Riesgo &laquo;Aprobación de la página profesional retrasada&raquo;</td><td><span class="chip warn">Abierto</span></td><td class="src">Riesgos &amp; Issues</td></tr>
      <tr><td>Tres obras con plazo y coste, fotografías y plugin de formularios</td><td><span class="chip warn">Pendiente</span> desde el 18/08</td><td class="src">Evidencia de la tarea</td></tr>
      <tr><td>Publicación de la página profesional</td><td><span class="chip warn">Pendiente</span> fijada al 11/09</td><td class="src">Plan de Acción, prioridad alta</td></tr>
    </tbody>
  </table></div>

  <h2>2. La restricción de calendario obliga a cortar el alcance</h2>
  <p>Del final de la sesión del día 8 (11:30) a la publicación del día 11 hay <b>dos días hábiles: miércoles 9 y jueves 10</b>. En esa ventana caben la actualización de plugins, la redacción y maquetación de los bloques repartidos, el mapa de redirecciones y el ensayo de publicación. No caben, además, los contenidos que dependen de datos que el cliente todavía no ha entregado.</p>
  <div class="tw"><table>
    <thead><tr><th>Se publica el 11/09 &mdash; MVP</th><th>Va a fase 2 &mdash; semanas del 15 y 22/09</th></tr></thead>
    <tbody>
      <tr><td>Bifurcación de entrada Profesional / Particular con conmutador permanente</td><td>Club de La Casa de Hormigón, ya acordado fuera de alcance el 17/08</td></tr>
      <tr><td>Página profesional B2B completa: cuatro perfiles del canal y formulario bifurcado con respuesta en menos de cinco minutos</td><td>Rangos de precio por metro cuadrado del recorrido particular, pendientes de validación comercial</td></tr>
      <tr><td>Dos o tres casos de obra, solo con los datos que el cliente confirme el día 8</td><td>Catálogo B2B completo con ficha por producto</td></tr>
      <tr><td>Catálogo B2B en versión mínima y reapuntado de las tres redirecciones provisionales</td><td>Calendario editorial, ya planificado al 25/09</td></tr>
    </tbody>
  </table></div>
  <div class="note">
    <p>Publicar el MVP el 11/09 cierra el riesgo de mayor probabilidad del programa &mdash;<em>el catálogo de producto B2B no tiene página viva y depende de un tercero</em>, impacto alto y probabilidad alta&mdash;, cuya mitigación registrada se fecha precisamente en esta publicación.</p>
  </div>

  <h2>3. Las ocho decisiones del 8 de septiembre</h2>
  <p>Cada una con opción por defecto, para que la sesión decida en lugar de deliberar.</p>
  <div class="tw"><table>
    <thead><tr><th class="num">#</th><th>Decisión</th><th>Opción por defecto de OSI</th><th>Si no se cierra</th></tr></thead>
    <tbody>
      <tr><td class="num">1</td><td class="k">Alcance del 11/09</td><td>MVP de la tabla anterior; el resto en dos fases</td><td>Se mueve la publicación</td></tr>
      <tr><td class="num">2</td><td class="k">Árbol de URLs y canónicas</td><td>URLs nuevas bajo la ruta profesional; la ruta provisional de colaboración con profesionales se reapunta a su destino definitivo el mismo 11/09</td><td>Se arrastran redirecciones provisionales y cadenas de saltos</td></tr>
      <tr><td class="num">3</td><td class="k">Casos de obra publicables</td><td>Bonanza, vivienda piloto de Valdemorillo y estructuras para promotoras, con plazo y superficie; coste en rango, no en cifra cerrada</td><td>Los bloques de prueba social se publican vacíos</td></tr>
      <tr><td class="num">4</td><td class="k">Plugin de formularios y campos</td><td>El que ya use producción; campos alineados con la taxonomía de perfiles, la pregunta de cómo nos ha conocido y el campo ORIGEN</td><td>El lead entra sin ORIGEN y no computa limpio</td></tr>
      <tr><td class="num">5</td><td class="k">Club de La Casa de Hormigón</td><td>Fuera del 11/09, documento y presupuesto aparte</td><td>Deriva de alcance hacia proyecto no contratado</td></tr>
      <tr><td class="num">6</td><td class="k">Futuro de la caché</td><td>Sustituir por caché de servidor en Plesk hasta que WP Rocket publique versión corregida</td><td>Se publica una estructura nueva sobre un sitio sin caché</td></tr>
      <tr><td class="num">7</td><td class="k">Reparto de redacción por bloques</td><td>Matriz del apartado 5, con entrega el <b>9/09 a las 20:00</b></td><td>No hay material que maquetar el día 10</td></tr>
      <tr><td class="num">8</td><td class="k">Firma del Go / No-Go</td><td>Javier (CVH) y OSI senior, el <b>10/09 a las 18:00</b></td><td>Se publica sin criterio de parada</td></tr>
    </tbody>
  </table></div>

  <h2>4. Bloqueantes técnicos antes de publicar</h2>

  <h3>4.1 Base WordPress</h3>
  <p>Detalle completo en la <em>Propuesta de mantenimiento web</em>, que se presenta a las 09:00 del mismo día. En resumen: 13 plugins pendientes, actualizaciones automáticas desactivadas, sitio sin caché desde el 24/08 y aviso de administrador dirigido a un buzón no vigilado. La ventana propuesta &mdash;semana del 1 al 8 de septiembre fuera de horario&mdash; ha quedado reducida a <b>la noche del 8 al 9</b>.</p>

  <h3>4.2 Medición</h3>
  <p>El sitio mide con un <b>contenedor de etiquetas que no controlan ni CVH ni OSI</b>, hallazgo abierto desde el 17/08. Si la estructura nueva se publica sin resolverlo, los eventos del formulario profesional pueden quedar sin trazar. El indicador contractual se calcula sobre el registro comercial, así que el bonus no está en riesgo; lo que se pierde es la capacidad de explicar de dónde vino cada lead.</p>
  <ul class="dash">
    <li>Reclamar el acceso al contenedor por escrito el día 8, o desplegar contenedor propio.</li>
    <li>Tomar la línea base de la web el <b>10/09</b>, con la estructura antigua todavía en producción.</li>
  </ul>

  <h3>4.3 Deuda de indexación</h3>
  <p>Complianz sirviendo una ruta de hoja de estilos sin resolver desde el 28/06, una URL con emoji en el slug y tres imágenes en error 404. Las tres entran en la ventana del 8 al 9: publicar encima sin corregirlas mantiene los errores en la cobertura de Search Console justo cuando se empieza a medir la estructura nueva.</p>

  <h2>5. Reparto de redacción por bloques</h2>
  <p>La estructura v1, redactada el 14/08, tiene <b>ocho bloques, cuatro perfiles del canal profesional, tres casos de obra citables y formulario bifurcado</b>. La matriz se rellena en la sesión contra ese documento; el criterio de reparto es el siguiente.</p>
  <div class="tw"><table>
    <thead><tr><th>Tipo de bloque</th><th>Redacta</th><th>Motivo</th><th>Entrega</th></tr></thead>
    <tbody>
      <tr><td>Argumentario técnico, certificaciones y especificaciones</td><td class="k">Javier (CVH)</td><td>Es dato de producto: no se puede escribir desde fuera</td><td>9/09 20:00</td></tr>
      <tr><td>Datos de las tres obras: plazo, superficie, rango de coste y fotografías</td><td class="k">Javier (CVH)</td><td>Dependencia crítica identificada desde el 18/08</td><td>9/09 20:00</td></tr>
      <tr><td>Los cuatro perfiles del canal profesional y su propuesta de valor</td><td class="k">OSI</td><td>Sale del Perfil de Cliente Objetivo v2</td><td>9/09 20:00</td></tr>
      <tr><td>Bloques de conversión: formulario, preacuerdo, tiempo de respuesta y WhatsApp centralizado</td><td class="k">OSI</td><td>Ya validados en la sesión del 20/08</td><td>9/09 20:00</td></tr>
      <tr><td>Textos legales, avisos y cookies</td><td class="k">OSI</td><td>Ligado a la corrección de Complianz</td><td>10/09 12:00</td></tr>
      <tr class="hl"><td>Maquetación e integración de todo</td><td class="k">OSI operación</td><td>&mdash;</td><td>10/09 18:00</td></tr>
    </tbody>
  </table></div>
  <div class="note caution">
    <p><b>Regla que conviene dejar dicha en la sesión.</b> Lo que no esté entregado el 9 de septiembre a las 20:00 no entra en la publicación del 11: se publica el bloque con la versión de OSI o se deja fuera. Sin esa regla, el día 10 se convierte en negociación en lugar de en maquetación.</p>
  </div>

  <h2>6. Cronograma</h2>
  <div class="tw"><table>
    <thead><tr><th>Fecha</th><th>Hora</th><th>Quién</th><th>Acción</th></tr></thead>
    <tbody>
      <tr><td>08/09</td><td>09:00&ndash;09:30</td><td>OSI &rarr; Cliente</td><td>Presentar la propuesta de mantenimiento y confirmar la ventana nocturna</td></tr>
      <tr><td>08/09</td><td>10:00&ndash;11:30</td><td>Ambos</td><td>Cerrar las ocho decisiones y el reparto de bloques</td></tr>
      <tr><td>08/09</td><td>mismo día</td><td>OSI</td><td>Enviar el acta con acuerdos y deberes, por escrito</td></tr>
      <tr class="hl"><td>08&rarr;09/09</td><td>noche</td><td>OSI operación</td><td>Copia previa &middot; 13 plugins de pruebas a producción &middot; Complianz &middot; slug con emoji &middot; imágenes en 404 &middot; buzón de avisos</td></tr>
      <tr><td>09/09</td><td>mañana</td><td>OSI</td><td>Verificación posterior: acceso, formularios, páginas no cacheadas y prueba de canales</td></tr>
      <tr class="hl"><td>09/09</td><td>20:00</td><td>Javier + OSI</td><td><b>Tope de entrega de textos y datos de obra</b></td></tr>
      <tr><td>10/09</td><td>09:00&ndash;18:00</td><td>OSI operación</td><td>Maquetación, mapa de redirecciones y revisión de medición</td></tr>
      <tr class="hl"><td>10/09</td><td>18:00</td><td>Javier + OSI senior</td><td><b>Go / No-Go</b> sobre la checklist del apartado 7</td></tr>
      <tr><td>10/09</td><td>18:00</td><td>OSI</td><td>Línea base de medición con la estructura antigua aún en producción</td></tr>
      <tr><td>11/09</td><td>fuera de horario</td><td>OSI operación</td><td>Copia previa, publicación, reapuntado de redirecciones y registro de cambios</td></tr>
      <tr><td>11/09</td><td>+2 h</td><td>OSI</td><td>Verificación en producción y solicitud de indexación en Search Console</td></tr>
      <tr><td>12&ndash;18/09</td><td>&mdash;</td><td>OSI</td><td>Vigilancia de cobertura, rendimiento y primeros leads del formulario</td></tr>
    </tbody>
  </table></div>

  <h2>7. Checklist Go / No-Go del 10/09 a las 18:00</h2>
  <p>Se publica solo si las nueve líneas están en verde.</p>
  <div class="tw"><table>
    <thead><tr><th class="num">#</th><th>Criterio</th><th>Verde</th></tr></thead>
    <tbody>
      <tr><td class="num">1</td><td>Copia de seguridad de la noche previa verificada y restaurable</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">2</td><td>Los 13 plugins actualizados en producción, con acceso, formularios y páginas no cacheadas comprobados</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">3</td><td>Complianz corregido: la ruta de la hoja de estilos resuelve y responde correctamente</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">4</td><td>Mapa de redirecciones cerrado, sin cadenas de más de un salto y sin destinos a portada</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">5</td><td>Formulario profesional enviando al buzón correcto, con ORIGEN, probado extremo a extremo</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">6</td><td>Medición resuelta: contenedor propio o acceso concedido, disparando el evento de envío</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">7</td><td>Textos y datos de obra entregados y maquetados, sin bloques con datos pendientes</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">8</td><td>Rendimiento aceptable en móvil en la página profesional, con la caché sustituta activa</td><td class="src">&#9744;</td></tr>
      <tr><td class="num">9</td><td>Registro de cambios abierto y aviso de administrador apuntando a buzón vigilado</td><td class="src">&#9744;</td></tr>
    </tbody>
  </table></div>
  <p>Si falla cualquiera de la 1 a la 6, <b>no se publica</b>: la publicación se mueve al 15/09. Si falla la 7, se publica el MVP recortado.</p>

  <h2>8. Indicadores</h2>
  <h3>8.1 Contractuales, sin cambios por esta publicación</h3>
  <ul class="dash">
    <li>Conversión final frente a la línea base <b>C0 = 0,8 %</b>, sellada en el acta firmada el 18/08 y medida sobre el total del registro.</li>
    <li>Mínimo de <b>25 presupuestos</b> en la ventana de medición final; estimación actual en torno a 42.</li>
    <li>Tres actas de hito aceptadas.</li>
  </ul>
  <h3>8.2 Operativos del protocolo, ya en uso</h3>
  <ul class="dash">
    <li>Tiempo de primera respuesta inferior a cinco minutos.</li>
    <li>Porcentaje de leads con ORIGEN informado en el CRM, hoy pendiente del partner de Odoo.</li>
    <li>Porcentaje de oportunidades con motivo de pérdida a 14 días.</li>
  </ul>
  <h3>8.3 De la web, nuevos</h3>
  <p>Línea base a tomar el <b>10/09</b>, antes de publicar.</p>
  <div class="tw"><table>
    <thead><tr><th>Indicador</th><th>Medición</th><th>Objetivo a 30 días</th></tr></thead>
    <tbody>
      <tr><td class="k">Leads del formulario profesional</td><td>Semanal</td><td>Tendencia al alza sobre la línea base del 10/09</td></tr>
      <tr><td class="k">Tasa de envío del formulario</td><td>Visitas a la página profesional frente a envíos</td><td>Establecer línea base y mejorarla</td></tr>
      <tr><td class="k">Páginas de la estructura nueva indexadas</td><td>Search Console, a 7 y 14 días</td><td>100 % de las URLs publicadas</td></tr>
      <tr><td class="k">Errores de cobertura</td><td>Search Console</td><td>Cero errores <em>nuevos</em> atribuibles a la publicación</td></tr>
      <tr><td class="k">Rendimiento en móvil de la página profesional</td><td>Antes y después</td><td>No degradar respecto al 10/09</td></tr>
      <tr><td class="k">URLs en error 404 tras la publicación</td><td>Registro de cambios</td><td>Cero</td></tr>
    </tbody>
  </table></div>

  <h2>9. Acciones de coste bajo y efecto inmediato</h2>
  <div class="tw"><table>
    <thead><tr><th>Acción</th><th>Efecto</th></tr></thead>
    <tbody>
      <tr><td class="k">Aviso de administrador a buzón vigilado</td><td>Cinco minutos de trabajo. Es lo único que separa una incidencia de una caída de cuatro días sin detectar</td></tr>
      <tr><td class="k">Corrección de Complianz</td><td>Cierra un error abierto desde el 28/06 que se arrastra en cobertura</td></tr>
      <tr><td class="k">Slug con emoji y su redirección</td><td>Recupera una URL que el buscador no reconoce</td></tr>
      <tr><td class="k">Tres imágenes en error 404</td><td>Recupera medios que llegaron a tener impresiones</td></tr>
      <tr><td class="k">Reapuntar las tres redirecciones provisionales</td><td>Aprovecha que la página destino ya existirá el 11/09</td></tr>
      <tr><td class="k">Reclamar el contenedor de medición</td><td>No cuesta nada, y sin él la web nueva nace ciega</td></tr>
    </tbody>
  </table></div>

  <h2>10. Impacto en integraciones</h2>
  <div class="tw"><table>
    <thead><tr><th>Integración</th><th>Efecto de la publicación</th><th>Qué vigilar</th></tr></thead>
    <tbody>
      <tr><td class="k">Search Console</td><td>URLs nuevas y redirecciones reapuntadas</td><td>Cobertura a 7 y 14 días; que el dominio canónico siga siendo el .es</td></tr>
      <tr><td class="k">GA4</td><td>Cambio en la estructura de rutas</td><td>Que los informes por página no se rompan; anotar la fecha de publicación</td></tr>
      <tr><td class="k">Contenedor de etiquetas</td><td>Contenedor ajeno</td><td><span class="chip bad">Bloqueante</span> resolver antes de publicar</td></tr>
      <tr><td class="k">Odoo &middot; registro de oportunidades</td><td>El formulario nuevo alimenta el CRM</td><td>Campos de perfil, importe y ORIGEN siguen pendientes del partner del cliente</td></tr>
      <tr><td class="k">Complianz</td><td>Consentimiento y textos legales</td><td>Que la corrección de la hoja de estilos no altere el banner</td></tr>
      <tr><td class="k">WhatsApp centralizado</td><td>En producción desde el 26/08</td><td>Prueba extremo a extremo tras actualizar plugins</td></tr>
      <tr><td class="k">Caché de servidor</td><td>Sustituta de WP Rocket</td><td>Purgado tras publicar, o se sirve la estructura antigua</td></tr>
    </tbody>
  </table></div>

  <h2>11. Guion de la sesión del 8 de septiembre</h2>
  <div class="tw"><table>
    <thead><tr><th>Hora</th><th class="num">Min</th><th>Punto</th><th>Qué tiene que salir</th></tr></thead>
    <tbody>
      <tr><td>10:00</td><td class="num">10</td><td class="k">Dónde estamos de verdad</td><td>Acuerdo explícito: o se cierra hoy, o se mueve el 11/09</td></tr>
      <tr><td>10:10</td><td class="num">15</td><td class="k">Material del cliente</td><td>Qué hay, qué falta y con qué fecha llega</td></tr>
      <tr><td>10:25</td><td class="num">20</td><td class="k">Acciones de OSI</td><td>Estructura entendida y sin objeciones abiertas</td></tr>
      <tr><td>10:45</td><td class="num">20</td><td class="k">Corte de alcance del 11/09</td><td>Decisiones 1 a 5</td></tr>
      <tr><td>11:05</td><td class="num">15</td><td class="k">Reparto de redacción</td><td>Decisión 7, con tope el 9/09 a las 20:00</td></tr>
      <tr><td>11:20</td><td class="num">10</td><td class="k">Gate del 11/09</td><td>Decisión 8 y checklist aceptada</td></tr>
    </tbody>
  </table></div>

  <h3>Insumos que se piden al cliente, con fecha</h3>
  <div class="tw"><table>
    <thead><tr><th>Insumo</th><th>Detalle</th><th>Tope</th></tr></thead>
    <tbody>
      <tr><td class="k">Tres obras publicables</td><td>Plazo real, superficie y coste en rango; no hace falta cifra cerrada</td><td>9/09 20:00</td></tr>
      <tr><td class="k">Fotografías</td><td>Mínimo dos por obra, en horizontal y con derechos para publicar</td><td>9/09 20:00</td></tr>
      <tr><td class="k">Argumentario técnico</td><td>Certificaciones y especificaciones que se pueden citar</td><td>9/09 20:00</td></tr>
      <tr><td class="k">Plugin de formularios</td><td>Cuál se usa y quién lo administra</td><td>En la sesión</td></tr>
      <tr><td class="k">Catálogo B2B</td><td>Qué se puede recuperar del proveedor y en qué plazo</td><td>En la sesión</td></tr>
      <tr><td class="k">Acceso al contenedor de etiquetas</td><td>O confirmación de que nadie en CVH lo controla</td><td>9/09</td></tr>
      <tr><td class="k">Campo ORIGEN en el CRM</td><td>Plazo comprometido del partner del cliente</td><td>En la sesión</td></tr>
    </tbody>
  </table></div>

  <h2>12. Acuerdos que debe recoger el acta</h2>
  <ul class="dash">
    <li>Ventana de mantenimiento aprobada: noche del 8 al 9, fuera de horario comercial.</li>
    <li>Política de actualizaciones y decisión sobre la caché.</li>
    <li>Buzón vigilado para el aviso de administrador, con dirección concreta.</li>
    <li>Alcance del 11/09 delimitado: qué entra en el MVP y qué va a fase 2.</li>
    <li>Las tres obras elegidas y los datos publicables de cada una.</li>
    <li>Club de La Casa de Hormigón confirmado fuera del alcance del 11/09.</li>
    <li>Reparto de bloques con responsable y tope del 9 de septiembre a las 20:00.</li>
    <li>Go / No-Go: Javier y OSI senior, 10/09 a las 18:00, sobre la checklist de nueve puntos.</li>
    <li>Plazos comprometidos para el contenedor de medición, el catálogo B2B y el campo ORIGEN del CRM.</li>
  </ul>

  <h2>13. Preparación de la sesión</h2>
  <h3>Material que se lleva</h3>
  <div class="tw"><table>
    <thead><tr><th>Documento</th><th>Estado</th></tr></thead>
    <tbody>
      <tr><td class="k">Propuesta de mantenimiento web</td><td><span class="chip ok">Listo</span> versión presentable, para el bloque de las 09:00</td></tr>
      <tr><td class="k">Este plan de ejecución</td><td><span class="chip ok">Listo</span></td></tr>
      <tr><td class="k">Propuesta «Nueva estructura web» (Opción A)</td><td><span class="chip ok">Listo</span> enviada por correo</td></tr>
      <tr><td class="k">Estructura v1 con los ocho bloques</td><td><span class="chip ok">Listo</span></td></tr>
      <tr><td class="k">Maqueta navegable bifurcada</td><td><span class="chip ok">Listo</span> con los datos pendientes marcados en ámbar</td></tr>
      <tr><td class="k">Matriz de reparto de bloques, impresa para rellenar a mano</td><td><span class="chip ok">Listo</span> apartado 5</td></tr>
      <tr><td class="k">Checklist Go / No-Go</td><td><span class="chip ok">Listo</span> apartado 7</td></tr>
    </tbody>
  </table></div>

  <h3>Pendientes de gestión antes del día 8</h3>
  <ul class="dash">
    <li><b>Confirmar el lugar de la reunión</b>: la convocatoria sigue como «presencial, lugar por confirmar».</li>
    <li><b>Actualizar la fecha objetivo</b> de la tarea de aprobación de estructura y contenidos, del 28/08 al 08/09, para que el retraso quede trazado y no simplemente vencido.</li>
  </ul>

  <p class="small">Documento de trabajo para la sesión del 08/09/2026. Estados y fechas tomados del espacio del programa a 04/09/2026. Programa de Crecimiento B2B &middot; Fase 3 &middot; Marca con garantía y página profesional.</p>
"""


DOCUMENTOS = [
    (
        "propuesta_mantenimiento_web_cvh.html",
        "Propuesta de mantenimiento web",
        "Actualización de plugins y política de mantenimiento, antes de la publicación del 11/09",
        "8 de septiembre de 2026 &middot; CVH PRECAST, S.L. (La Casa de Hormigón) &middot; Programa de Crecimiento B2B &middot; Fase 3",
        "Propuesta de mantenimiento web &middot; 08/09/2026",
        MANTENIMIENTO,
    ),
    (
        "plan_ejecucion_web_cvh.html",
        "Plan de ejecución de la nueva estructura web",
        "Opción A &middot; Doble puerta: Profesionales y Particulares, con el Club por fases",
        "Sesión del 8 de septiembre de 2026 &middot; publicación prevista el 11/09 &middot; CVH PRECAST, S.L. (La Casa de Hormigón)",
        "Plan de ejecución web &middot; sesión del 08/09/2026",
        PLAN,
    ),
]


CHROMIUM = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "chromium",
    "chromium-browser",
    "google-chrome",
]


def navegador():
    """Primer Chromium disponible, o None si no hay ninguno."""
    for candidato in CHROMIUM:
        ruta = candidato if pathlib.Path(candidato).exists() else shutil.which(candidato)
        if ruta:
            return ruta
    return None


def a_pdf(navegador_bin, html):
    """Imprime el HTML a PDF con los márgenes de la hoja A4 del documento."""
    pdf = html.with_suffix(".pdf")
    subprocess.run(
        [
            navegador_bin,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf}",
            html.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    return pdf


def main():
    bin_navegador = navegador()
    if not bin_navegador:
        print("Aviso: sin Chromium disponible, solo se genera el HTML.")

    for nombre, titulo, subtitulo, meta, pie, cuerpo in DOCUMENTOS:
        destino = SALIDA / nombre
        destino.write_text(
            documento(titulo, subtitulo, meta, cuerpo, pie), encoding="utf-8"
        )
        print(f"{destino.relative_to(RAIZ)} · {destino.stat().st_size // 1024} KB")
        if bin_navegador:
            pdf = a_pdf(bin_navegador, destino)
            print(f"{pdf.relative_to(RAIZ)} · {pdf.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
