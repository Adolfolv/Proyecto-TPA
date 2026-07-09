import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request


class ClienteGemini:
    """Cliente REST minimo para consultar Gemini sin acoplar la vista a la API."""

    URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    API_KEY_REPOSITORIO = ""

    def __init__(self, api_key=None, modelo=None, timeout=25, reintentos=2):
        self.api_key = self._resolver_api_key(api_key)
        self.modelo = modelo or os.getenv("GEMINI_MODELO", "gemini-2.5-flash-lite")
        self.timeout = timeout
        self.reintentos = reintentos

    def _resolver_api_key(self, api_key):
        if api_key:
            return self._limpiar_api_key(api_key)

        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("AYUDA_IA_API_KEY")
        if api_key:
            return self._limpiar_api_key(api_key)

        archivo_clave = Path.home() / ".movilidad_gemini_key"
        if archivo_clave.exists():
            return self._limpiar_api_key(archivo_clave.read_text(encoding="utf-8"))

        return self._limpiar_api_key(self.API_KEY_REPOSITORIO)

    def _limpiar_api_key(self, api_key):
        return api_key.strip().lstrip("\ufeff")

    def generar_respuesta(self, instruccion_sistema, pregunta):
        if not self.api_key:
            raise ValueError("No se encontró la clave GEMINI_API_KEY o AYUDA_IA_API_KEY.")

        datos = {
            "systemInstruction": {"parts": [{"text": instruccion_sistema}]},
            "contents": [{"role": "user", "parts": [{"text": pregunta}]}],
            "generationConfig": {"temperature": 0.25, "maxOutputTokens": 2048},
        }
        cuerpo = json.dumps(datos).encode("utf-8")
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        for intento in range(self.reintentos + 1):
            solicitud = urllib.request.Request(self.URL_BASE.format(modelo=self.modelo), data=cuerpo, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(solicitud, timeout=self.timeout) as respuesta:
                    return self._extraer_texto(json.loads(respuesta.read().decode("utf-8")))
            except urllib.error.HTTPError as error:
                detalle = error.read().decode("utf-8", errors="ignore")
                espera, indicada = self._obtener_espera(error, detalle, intento)
                if error.code in (429, 503) and intento < self.reintentos and (not indicada or espera <= 8):
                    time.sleep(espera)
                    continue
                raise RuntimeError(self._mensaje_error_http(error.code, detalle, espera if indicada else None)) from error
            except urllib.error.URLError as error:
                raise RuntimeError(f"No se pudo conectar con Gemini: {error.reason}") from error

    def _obtener_espera(self, error, detalle, intento):
        valor_header = error.headers.get("Retry-After") if error.headers else None
        if valor_header:
            try:
                return float(valor_header), True
            except ValueError:
                pass
        try:
            detalles = json.loads(detalle).get("error", {}).get("details", [])
            for item in detalles:
                if str(item.get("@type", "")).endswith("RetryInfo"):
                    return float(str(item.get("retryDelay", "0s")).rstrip("s")), True
        except (ValueError, TypeError, json.JSONDecodeError):
            pass
        return min(2 ** intento, 4), False

    def _mensaje_error_http(self, codigo, detalle, espera=None):
        try:
            mensaje_api = json.loads(detalle).get("error", {}).get("message", "")
        except json.JSONDecodeError:
            mensaje_api = ""
        if codigo == 401:
            return "La clave de Gemini no es válida. Configura GEMINI_API_KEY o AYUDA_IA_API_KEY con una clave activa."
        if codigo == 403:
            return "La clave de Gemini no tiene permisos para este modelo o proyecto. Revisa la API key y la facturación en Google AI Studio."
        if codigo == 429:
            reintento = f" Intenta nuevamente en {max(int(espera), 1)} segundos." if espera else " Espera unos minutos e intenta nuevamente."
            return "Gemini alcanzó el límite de solicitudes de este proyecto." + reintento + " Si continúa, revisa la cuota o la facturación en Google AI Studio."
        if codigo == 503:
            return "Gemini está temporalmente saturado. Espera unos segundos e intenta nuevamente."
        return f"Gemini respondió con error {codigo}: {mensaje_api or 'no fue posible completar la consulta.'}"

    def _extraer_texto(self, payload):
        candidatos = payload.get("candidates", [])
        if not candidatos:
            return "No pude generar una respuesta con la consulta enviada."

        partes = candidatos[0].get("content", {}).get("parts", [])
        textos = [parte.get("text", "") for parte in partes if parte.get("text")]
        return "\n".join(textos).strip() or "No pude generar una respuesta con la consulta enviada."
