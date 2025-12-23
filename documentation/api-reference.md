# Babel API Reference

Integrate Babel's translation capabilities into your applications with our RESTful API.

> **Note**: API access requires a **Growth** or **Business** plan.

---

## Authentication

All API requests require an API key passed in the `Authorization` header:

```bash
Authorization: Bearer YOUR_API_KEY
```

Generate your API key in the [Dashboard Settings](dashboard/account/index.html).

---

## Base URL

```
https://api.babel.app/v1
```

---

## Endpoints

### Translate Document

Upload a file for translation.

**POST** `/translate`

#### Request

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file` | File | Yes | The document to translate (PDF, DOCX, PPTX, TXT) |
| `target_language` | String | Yes | Target language code (e.g., `es`, `fr`, `zh-CN`) |
| `source_language` | String | No | Source language code (auto-detected if omitted) |
| `output_format` | String | No | `translated` (default) or `bilingual` |
| `glossary_id` | String | No | ID of a custom glossary to apply |

#### Example

```bash
curl -X POST https://api.babel.app/v1/translate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@document.pdf" \
  -F "target_language=es" \
  -F "output_format=bilingual"
```

#### Response

```json
{
  "job_id": "abc123-def456-ghi789",
  "status": "processing",
  "estimated_credits": 5420,
  "estimated_completion": "2024-01-15T10:35:00Z"
}
```

---

### Check Job Status

Get the status of a translation job.

**GET** `/jobs/{job_id}`

#### Example

```bash
curl https://api.babel.app/v1/jobs/abc123-def456-ghi789 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Response (Processing)

```json
{
  "job_id": "abc123-def456-ghi789",
  "status": "processing",
  "progress": 45,
  "message": "Translating page 12 of 27..."
}
```

#### Response (Complete)

```json
{
  "job_id": "abc123-def456-ghi789",
  "status": "completed",
  "progress": 100,
  "credits_used": 5420,
  "download_url": "https://api.babel.app/v1/download/abc123-def456-ghi789",
  "expires_at": "2024-01-16T10:30:00Z"
}
```

---

### Download Translated File

Download the completed translation.

**GET** `/download/{job_id}`

#### Example

```bash
curl -O https://api.babel.app/v1/download/abc123-def456-ghi789 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

### List Jobs

Get a list of your translation jobs.

**GET** `/jobs`

#### Query Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `status` | String | Filter by status: `pending`, `processing`, `completed`, `failed` |
| `limit` | Integer | Number of results (default: 20, max: 100) |
| `offset` | Integer | Pagination offset |

#### Example

```bash
curl "https://api.babel.app/v1/jobs?status=completed&limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

### Get Credit Balance

Check your remaining credits.

**GET** `/account/credits`

#### Response

```json
{
  "plan": "Growth",
  "credits_total": 2000000,
  "credits_used": 845000,
  "credits_remaining": 1155000,
  "resets_at": "2024-02-01T00:00:00Z"
}
```

---

## Glossaries

### Create Glossary

Upload a custom glossary for consistent terminology.

**POST** `/glossaries`

#### Request

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | Yes | Glossary name |
| `file` | File | Yes | CSV file with `source,target` columns |
| `source_language` | String | Yes | Source language code |
| `target_language` | String | Yes | Target language code |

#### Example

```bash
curl -X POST https://api.babel.app/v1/glossaries \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "name=Legal Terms EN-DE" \
  -F "file=@legal-glossary.csv" \
  -F "source_language=en" \
  -F "target_language=de"
```

---

### List Glossaries

**GET** `/glossaries`

---

### Delete Glossary

**DELETE** `/glossaries/{glossary_id}`

---

## Error Codes

| Code | Description |
| :--- | :--- |
| `400` | Bad Request - Invalid parameters |
| `401` | Unauthorized - Invalid or missing API key |
| `402` | Payment Required - Insufficient credits |
| `404` | Not Found - Job or resource doesn't exist |
| `413` | Payload Too Large - File exceeds 100MB limit |
| `429` | Rate Limited - Too many requests |
| `500` | Server Error - Contact support |

---

## Rate Limits

| Plan | Requests/Minute | Concurrent Jobs |
| :--- | :--- | :--- |
| Growth | 60 | 10 |
| Business | 300 | 50 |

---

## Webhooks

Configure webhooks to receive notifications when jobs complete.

**POST** `/webhooks`

```json
{
  "url": "https://your-app.com/babel-webhook",
  "events": ["job.completed", "job.failed"]
}
```

When a job completes, we'll POST to your URL:

```json
{
  "event": "job.completed",
  "job_id": "abc123-def456-ghi789",
  "download_url": "https://api.babel.app/v1/download/abc123-def456-ghi789",
  "credits_used": 5420
}
```
