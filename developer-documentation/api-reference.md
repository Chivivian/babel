# API Reference

This document provides a complete reference for the Babel Translation Server API. It covers all available endpoints, their parameters, expected responses, and error codes.

---

## Base URL

When running locally, the server is available at:
```
http://localhost:8000
```

---

## Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/translate` | Submit a document for translation |
| `GET` | `/api/job/{job_id}` | Check the status of a translation job |
| `GET` | `/api/translations` | List all translation jobs |
| `GET` | `/api/download/{filename}` | Download a translated file |
| `GET` | `/api/view/{filename}` | View a translated PDF in the browser |

---

## Endpoint Details

### `POST /api/translate`

Submits a document for translation. The request must be sent as `multipart/form-data`.

#### Request Parameters

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file` | File | Yes | The PDF document to translate. |
| `target_language` | String | Yes | The ISO 639-1 language code (e.g., `es`, `fr`, `de`). |

#### Example Request (cURL)

```bash
curl -X POST "http://localhost:8000/api/translate" \
  -F "file=@/path/to/your/document.pdf" \
  -F "target_language=es"
```

#### Success Response (200 OK)

```json
{
  "status": "success",
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Translation started"
}
```

The `job_id` is a unique identifier (UUID) that you will use to poll the status of the translation.

---

### `GET /api/job/{job_id}`

Retrieves the current status and progress of a translation job.

#### Path Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `job_id` | String | The unique job identifier returned from `/api/translate`. |

#### Example Request

```bash
curl "http://localhost:8000/api/job/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

#### Response Examples

**In Progress:**
```json
{
  "job_id": "a1b2c3d4-...",
  "status": "processing",
  "progress": 45,
  "message": "Translating content...",
  "original_filename": "document.pdf",
  "target_language": "es",
  "translated_file": null,
  "error": null,
  "created_at": "2025-11-19T10:30:00.000Z",
  "completed_at": null
}
```

**Completed:**
```json
{
  "job_id": "a1b2c3d4-...",
  "status": "completed",
  "progress": 100,
  "message": "Translation complete!",
  "original_filename": "document.pdf",
  "target_language": "es",
  "translated_file": "document.es.mono.pdf",
  "error": null,
  "created_at": "2025-11-19T10:30:00.000Z",
  "completed_at": "2025-11-19T10:35:00.000Z"
}
```

**Failed:**
```json
{
  "job_id": "a1b2c3d4-...",
  "status": "failed",
  "progress": 12,
  "message": "Translation failed",
  "error": "OpenAI API rate limit exceeded",
  ...
}
```

---

### `GET /api/translations`

Returns a list of all translation jobs, sorted by creation time (newest first). Useful for the "My Translations" dashboard page.

#### Example Request

```bash
curl "http://localhost:8000/api/translations"
```

#### Success Response

```json
{
  "count": 5,
  "translations": [
    { "job_id": "...", "status": "completed", ... },
    { "job_id": "...", "status": "processing", ... }
  ]
}
```

---

### `GET /api/download/{filename}`

Downloads the translated PDF file.

#### Path Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `filename` | String | The name of the translated file (from the `translated_file` field). |

#### Example

```bash
curl -O "http://localhost:8000/api/download/document.es.mono.pdf"
```

---

### `GET /api/view/{filename}`

Opens the translated PDF in the browser for inline viewing (no download prompt).

#### Example

```
http://localhost:8000/api/view/document.es.mono.pdf
```

---

## Job Status Codes

| Status | Description |
| :--- | :--- |
| `pending` | Job has been created but not yet started. |
| `processing` | Translation is in progress. Poll for `progress` updates. |
| `completed` | Translation finished successfully. `translated_file` is available. |
| `failed` | Translation failed. Check the `error` field for details. |

---

## Error Handling

All errors are returned as JSON with an appropriate HTTP status code.

| HTTP Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – Missing or invalid parameters. |
| `404` | Not Found – Job ID or file not found. |
| `500` | Internal Server Error – Check the `error` field for details. |

#### Example Error Response

```json
{
  "detail": "Job not found"
}
```

---

## Polling Strategy

When a job is submitted, the frontend should poll `/api/job/{job_id}` at regular intervals to update the UI.

**Recommended Polling Interval:** 2-3 seconds.

The `progress` field (0-100) can be used to drive a progress bar. The `message` field provides human-readable status updates.

---

## Rate Limits

The Babel API currently does not enforce rate limits for local development. In production, API calls are metered per-translation based on the pricing tier (see the main documentation).
