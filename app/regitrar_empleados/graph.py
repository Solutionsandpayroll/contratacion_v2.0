"""
Envío de correos vía Microsoft Graph API (reemplazo del flujo de Power Automate
'Enviar_correo_electrónico_(V2)').

Reutiliza el mismo patrón de autenticación (client credentials + cache de token)
que graph_pdf_utils.py, para no tener dos formas distintas de autenticarse
contra Graph dentro del proyecto.
"""

import base64
import time
import requests
import os


TENANT = os.environ.get("GRAPH_TENANT_ID")
CLIENT = os.environ.get("GRAPH_CLIENT_ID")
SECRET = os.environ.get("GRAPH_CLIENT_SECRET")

# Buzón/remitente desde el cual se envían los correos.
# Debe ser un usuario válido del tenant (licenciado con Exchange Online) y la
# app registrada debe tener permiso de aplicación Mail.Send sobre Graph.
REMITENTE = "noreply@solutionsandpayroll.com"  # <-- ajusta esto si aplica

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

# ── Cache simple de token en memoria (compartido conceptualmente con el otro
# módulo de Graph, aunque aquí se mantiene independiente a propósito) ──
_token_cache = {"token": None, "expira": 0}


def _obtener_token():
    """Devuelve un token válido, reutilizando el cacheado si no ha expirado."""
    ahora = time.time()
    if _token_cache["token"] and ahora < _token_cache["expira"] - 60:
        return _token_cache["token"]

    url = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token"
    datos = {
        "grant_type": "client_credentials",
        "client_id": CLIENT,
        "client_secret": SECRET,
        "scope": "https://graph.microsoft.com/.default",
    }
    resp = requests.post(url, data=datos, timeout=30)
    resp.raise_for_status()
    payload = resp.json()

    _token_cache["token"] = payload["access_token"]
    _token_cache["expira"] = ahora + payload.get("expires_in", 3600)
    return _token_cache["token"]


def _headers():
    return {
        "Authorization": f"Bearer {_obtener_token()}",
        "Content-Type": "application/json",
    }


def _construir_adjuntos_graph(adjuntos):
    """
    Convierte la lista de adjuntos que ya arma la vista (vía archivo_a_base64)
    al formato que espera Graph para fileAttachment.

    Entrada esperada (igual a la que ya usabas para Power Automate):
        [{"nombre": "...", "contenido": "<base64>", "tipo": "..."}, ...]
    """
    resultado = []
    for adj in adjuntos or []:
        resultado.append({
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": adj.get("nombre") or "adjunto",
            "contentType": adj.get("tipo") or "application/octet-stream",
            "contentBytes": adj.get("contenido", ""),
        })
    return resultado


def enviar_correo_via_graph(destinatario, asunto, cuerpo_html, adjuntos=None, remitente=None):
    """
    Envía un correo usando Microsoft Graph (POST /users/{remitente}/sendMail).

    Equivalente directo del payload que antes se mandaba a Power Automate:
        {
            "destinatario": ...,
            "estructura": ...,     # ya no se usa aquí: la plantilla se resuelve
                                    # en la vista antes de llamar a esta función
            "asunto": ...,
            "cuerpo_html": ...,
            "adjuntos": [...]
        }

    Parámetros
    ----------
    destinatario : str            -> correo del destinatario
    asunto       : str
    cuerpo_html  : str             -> HTML ya resuelto (como el que arma el
                                       editor contenteditable en el modal)
    adjuntos     : list[dict]      -> [{"nombre", "contenido" (b64), "tipo"}, ...]
    remitente    : str | None      -> buzón emisor; por defecto REMITENTE

    Retorna
    -------
    requests.Response
        Para mantener compatibilidad con el código de la vista, que revisa
        `respuesta.status_code`. Graph responde 202 Accepted sin cuerpo si
        todo salió bien.
    """
    remitente = remitente or REMITENTE

    mensaje = {
        "message": {
            "subject": asunto,
            "body": {
                "contentType": "HTML",
                "content": f'<p class="editor-paragraph">{cuerpo_html}</p>',
            },
            "toRecipients": [
                {"emailAddress": {"address": destinatario}}
            ],
            "attachments": _construir_adjuntos_graph(adjuntos),
        },
        "saveToSentItems": "true",
    }

    url = f"{GRAPH_BASE}/users/{remitente}/sendMail"
    resp = requests.post(url, headers=_headers(), json=mensaje, timeout=120)
    return resp