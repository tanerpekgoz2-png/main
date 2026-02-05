# Tek Taraflı Geçiş İçin Kamera + Bulut Plaka Tanıma (MVP)

Bu proje, **tek yönlü (tek taraflı) geçiş** senaryosu için kamera verisi ve bulut tabanlı OCR kullanarak plaka tanıma akışı sunan örnek bir servistir.

## Neler var?

- FastAPI tabanlı HTTP servis
- Araç izine (`track_id`) göre tek yön geçiş doğrulama
- Geçiş doğrulandıktan sonra bulut OCR entegrasyonu
- Bulut OCR kapalıysa metin ipucundan (hint) regex tabanlı plaka çıkarımı
- Birim testler (yön filtresi)

## Mimari

1. Kamera/edge katmanı araç takibini yapar ve `track_id`, `centroid_x` gibi metrikleri üretir.
2. Bu servis `DirectionGate` ile aracın doğru yönde geçip geçmediğini doğrular.
3. Araç doğrulandıysa görüntü, bulut OCR servisine gönderilir.
4. Dönen metinden plaka normalize edilerek API cevabına yazılır.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
uvicorn src.plaka_sistem.main:app --reload --port 8000
```

## Örnek istek

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": "cam-01",
    "track_id": "veh-1001",
    "centroid_x": 410,
    "image_base64": null,
    "ocr_text_hint": "34 ABC 123"
  }'
```

> Not: Geçişin doğrulanması için aynı `track_id` için önce giriş çizgisine yakın, sonra çıkış çizgisine yakın `centroid_x` değerleri gönderilmelidir.

## Konfigürasyon (env)

- `ALLOWED_DIRECTION`: `left_to_right` veya `right_to_left` (varsayılan `left_to_right`)
- `ENTER_LINE_X`: Giriş çizgisi (varsayılan `120`)
- `EXIT_LINE_X`: Çıkış çizgisi (varsayılan `380`)
- `MIN_DELTA_X`: Minimum x değişimi (varsayılan `120`)
- `OCR_ENDPOINT`: Bulut OCR endpoint'i (opsiyonel)
- `OCR_API_KEY`: Bulut OCR API anahtarı (opsiyonel)

## Test

```bash
pytest -q
```
