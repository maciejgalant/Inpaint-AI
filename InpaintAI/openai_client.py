import base64
import json

from qgis.PyQt.QtCore import QObject, pyqtSignal, QUrl, QFile, QByteArray
from qgis.PyQt.QtNetwork import (
    QNetworkRequest, QHttpMultiPart, QHttpPart, QNetworkReply
)
from qgis.core import QgsApplication, QgsNetworkAccessManager


API_URL = "https://api.openai.com/v1/images/edits"
IMAGE_REQUEST_TIMEOUT_MS = 15 * 60 * 1000  # 15 minutes for xhigh/max edits

MODEL_IDS = {
    "Sunburst — precyzyjna edycja": "gpt-image-2.5-sunburst",
    "Flare — szybka generacja": "gpt-image-2.5-flare",
}


class OpenAICloudClient(QObject):
    finished = pyqtSignal(bytes, str)   # image bytes, request id
    failed = pyqtSignal(str)
    progress = pyqtSignal(int, str)

    def __init__(self, parent=None):
        # QObject requires another QObject (or None) as its parent.  Older
        # plugin builds passed the Python plugin instance here, which caused a
        # TypeError before the API request was even created.  Accept such
        # callers safely by dropping an invalid parent.
        if parent is not None and not isinstance(parent, QObject):
            parent = None
        super().__init__(parent)
        self.reply = None
        self.multipart = None
        self._previous_qgis_timeout = None
        self._timeout_override_active = False

    def _enable_long_request_timeout(self):
        """Temporarily raise QGIS' global network timeout for long image edits.

        QGIS defaults to roughly 60 seconds. GPT Image high/xhigh/max edits can
        legitimately take longer, so the plugin raises it only for the duration
        of this request and restores the previous user setting afterwards.
        """
        if self._timeout_override_active:
            return
        try:
            current = int(QgsNetworkAccessManager.timeout())
        except Exception:
            current = 60000
        self._previous_qgis_timeout = current
        try:
            if current != 0 and current < IMAGE_REQUEST_TIMEOUT_MS:
                QgsNetworkAccessManager.setTimeout(IMAGE_REQUEST_TIMEOUT_MS)
                self._timeout_override_active = True
        except Exception:
            self._previous_qgis_timeout = None
            self._timeout_override_active = False

    def _restore_network_timeout(self):
        if not self._timeout_override_active:
            return
        try:
            if self._previous_qgis_timeout is not None:
                QgsNetworkAccessManager.setTimeout(self._previous_qgis_timeout)
        finally:
            self._previous_qgis_timeout = None
            self._timeout_override_active = False

    @staticmethod
    def _text_part(name, value):
        part = QHttpPart()
        part.setRawHeader(
            b"Content-Disposition",
            f'form-data; name="{name}"'.encode("utf-8")
        )
        part.setBody(str(value).encode("utf-8"))
        return part

    @staticmethod
    def _file_part(name, path, filename):
        file_obj = QFile(str(path))
        if not file_obj.open(QFile.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Nie można otworzyć pliku: {path}")

        part = QHttpPart()
        part.setRawHeader(
            b"Content-Disposition",
            f'form-data; name="{name}"; filename="{filename}"'.encode("utf-8")
        )
        part.setRawHeader(b"Content-Type", b"image/png")
        part.setBodyDevice(file_obj)
        return part, file_obj

    def edit_image(self, image_path, mask_path, prompt, authcfg,
                   model_id, quality="medium", size="1024x1024"):
        if self.reply is not None:
            raise RuntimeError("Poprzednie żądanie nadal trwa.")
        if not authcfg:
            raise RuntimeError("Nie wybrano konfiguracji uwierzytelniania QGIS.")

        self.progress.emit(50, "Przygotowanie żądania OpenAI…")

        multipart = QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
        multipart.append(self._text_part("model", model_id))
        multipart.append(self._text_part("prompt", prompt))
        multipart.append(self._text_part("quality", quality))
        multipart.append(self._text_part("size", size))

        image_part, image_file = self._file_part(
            "image[]", image_path, "orthophoto.png"
        )
        mask_part, mask_file = self._file_part(
            "mask", mask_path, "mask.png"
        )
        image_file.setParent(multipart)
        mask_file.setParent(multipart)
        multipart.append(image_part)
        multipart.append(mask_part)

        request = QNetworkRequest(QUrl(API_URL))
        request.setRawHeader(b"Accept", b"application/json")

        auth_manager = QgsApplication.authManager()
        if not auth_manager.updateNetworkRequest(request, authcfg):
            multipart.deleteLater()
            raise RuntimeError(
                "QGIS nie zastosował wybranej konfiguracji uwierzytelniania. "
                "Upewnij się, że jest to konfiguracja typu API Header."
            )

        # QGIS' normal network timeout is too short for high/xhigh/max image edits.
        # A request-specific Qt timeout is set as well as a temporary QGIS timeout
        # override, because QGIS maintains its own timeout timer.
        try:
            request.setTransferTimeout(IMAGE_REQUEST_TIMEOUT_MS)
        except (AttributeError, TypeError):
            pass

        self._enable_long_request_timeout()
        try:
            nam = QgsNetworkAccessManager.instance()
            reply = nam.post(request, multipart)
        except Exception:
            self._restore_network_timeout()
            multipart.deleteLater()
            raise

        multipart.setParent(reply)

        self.multipart = multipart
        self.reply = reply
        wait_text = "Wysłano crop i maskę — oczekiwanie na model…"
        if quality in ("xhigh", "max"):
            wait_text += " Tryb wysokiej jakości może potrwać kilka minut."
        self.progress.emit(60, wait_text)
        reply.finished.connect(self._on_finished)

    def cancel(self):
        if self.reply is not None:
            self.reply.abort()

    def _on_finished(self):
        reply = self.reply
        self.reply = None
        self.multipart = None
        self._restore_network_timeout()

        if reply is None:
            return

        status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        request_id = bytes(reply.rawHeader(b"x-request-id")).decode("utf-8", "ignore")
        body = bytes(reply.readAll())
        network_error = reply.error()
        network_error_text = reply.errorString()
        reply.deleteLater()

        # PyQt6 enum NetworkError.NoError may still be truthy in Python.
        # Compare explicitly instead of using `if network_error:`.
        http_failed = status is not None and int(status) >= 400
        network_failed = network_error != QNetworkReply.NetworkError.NoError

        if http_failed or network_failed:
            detail = network_error_text
            try:
                payload = json.loads(body.decode("utf-8"))
                detail = payload.get("error", {}).get("message", detail)
            except Exception:
                pass
            self.failed.emit(
                f"Błąd OpenAI / sieci"
                + (f" (HTTP {status})" if status else "")
                + f":\n{detail}"
                + (f"\nRequest ID: {request_id}" if request_id else "")
            )
            return

        try:
            payload = json.loads(body.decode("utf-8"))
            image_b64 = payload["data"][0]["b64_json"]
            image_bytes = base64.b64decode(image_b64)
        except Exception as exc:
            self.failed.emit(
                f"OpenAI zwróciło odpowiedź, ale nie udało się odczytać obrazu: {exc}"
            )
            return

        self.progress.emit(85, "Obraz odebrany — georeferencja…")
        self.finished.emit(image_bytes, request_id)
