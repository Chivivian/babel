# Version 0.1.2 - Multi-Model Integration

**Status:** Planned  
**Target Release:** TBD  
**Depends On:** Version 0.1.1

---

## Overview

Version 0.1.2 focuses on expanding Babel's LLM support beyond OpenAI to include **Mistral AI** and **Google Gemini** models. This will give users more flexibility in choosing translation models based on cost, speed, and quality requirements.

---

## New Models to Integrate

### Mistral Models

| Model | Parameters | Context | Best For | Est. Cost |
|:---|:---|:---|:---|:---|
| **Mistral Small 3** | 24B | 32K tokens | Fast, cost-effective translations | Very Low |
| **Mistral Medium** | ~70B | 32K tokens | Balanced quality/cost | Low |
| **Mistral Large** | 123B | 128K tokens | High-quality, complex documents | Medium |

### Google Gemini Models

| Model | Context | Best For | Est. Cost |
|:---|:---|:---|:---|
| **Gemini 2.0 Flash** | 1M tokens | Ultra-fast, cost-effective | Very Low |
| **Gemini 2.0 Pro** | 2M tokens | High-quality, long documents | Medium |
| **Gemini 3.0 Flash** | 1M tokens | Next-gen speed, improved accuracy | Low |
| **Gemini 3.0 Pro** | 2M tokens | State-of-the-art quality | Medium-High |

### Model Comparison (All Providers)

| Model | Provider | Quality | Speed | Cost | Recommended Use |
|:---|:---|:---|:---|:---|:---|
| gpt-4o-mini | OpenAI | ★★★★☆ | Fast | Low | Default, general use |
| gpt-4o | OpenAI | ★★★★★ | Fast | High | Premium, critical docs |
| mistral-small-3 | Mistral | ★★★☆☆ | Very Fast | Very Low | Bulk processing |
| mistral-medium | Mistral | ★★★★☆ | Fast | Low | Cost-conscious quality |
| mistral-large | Mistral | ★★★★★ | Medium | Medium | Alternative to GPT-4o |
| gemini-2.0-flash | Google | ★★★★☆ | Very Fast | Very Low | Speed priority, long docs |
| gemini-2.0-pro | Google | ★★★★★ | Fast | Medium | Long documents, high quality |
| gemini-3.0-flash | Google | ★★★★★ | Very Fast | Low | Next-gen speed + quality |
| gemini-3.0-pro | Google | ★★★★★ | Fast | Medium-High | Best quality, long docs |

---

## Implementation Requirements

### 1. Mistral API Integration

**File:** `babel-backend/BabelDOC-main/` (translation engine)

Add support for Mistral API alongside existing OpenAI integration:

```python
# New command-line flags
--mistral                    # Use Mistral API
--mistral-model MODEL        # Model selection (default: mistral-small-3)
--mistral-api-key KEY        # API key (or use MISTRAL_API_KEY env var)
```

### 2. Environment Configuration

**File:** `babel-backend/.env`

Add new environment variable:

```bash
OPENAI_API_KEY=sk-...
MISTRAL_API_KEY=...          # New
GOOGLE_API_KEY=...           # New (for Gemini)
```

### 3. CLI Updates

**File:** `translate.py`

Update the translation script to support model provider selection:

```bash
# OpenAI (existing)
python translate.py doc.pdf --lang fr --model gpt-4o-mini

# Mistral (new)
python translate.py doc.pdf --lang fr --provider mistral --model mistral-small-3
python translate.py doc.pdf --lang fr --provider mistral --model mistral-medium
python translate.py doc.pdf --lang fr --provider mistral --model mistral-large

# Google Gemini (new)
python translate.py doc.pdf --lang fr --provider google --model gemini-2.0-flash
python translate.py doc.pdf --lang fr --provider google --model gemini-2.0-pro
```

### 4. API Endpoint Updates

**File:** `babel-backend/server.py`

Add optional `model` and `provider` parameters to the `/api/translate` endpoint:

```json
{
  "file": "<binary>",
  "target_language": "fr",
  "provider": "google",         // "openai" (default), "mistral", or "google"
  "model": "gemini-2.0-flash"   // specific model selection
}
```

---

## Development Checklist

- [ ] **Mistral API Client**
  - [ ] Implement Mistral API wrapper
  - [ ] Handle authentication and error responses
  - [ ] Match OpenAI response format for compatibility

- [ ] **Google Gemini API Client**
  - [ ] Implement Gemini API wrapper
  - [ ] Handle authentication via Google API key
  - [ ] Support 1M+ token context windows

- [ ] **CLI Integration**
  - [ ] Add `--provider` flag to `translate.py`
  - [ ] Support provider values: `openai`, `mistral`, `google`
  - [ ] Update help text and documentation

- [ ] **Server Integration**
  - [ ] Add provider/model to `/api/translate` endpoint
  - [ ] Update job status to include model information

- [ ] **Configuration**
  - [ ] Add `MISTRAL_API_KEY` to `.env.example`
  - [ ] Add `GOOGLE_API_KEY` to `.env.example`
  - [ ] Update setup guide

- [ ] **Testing**
  - [ ] Test each Mistral model with sample documents
  - [ ] Test each Gemini model with sample documents
  - [ ] Compare quality against GPT-4o-mini baseline
  - [ ] Test Gemini with very long documents (1M+ tokens)

- [ ] **Documentation**
  - [ ] Update worker-orchestration.md with new models
  - [ ] Add Mistral and Gemini to API reference
  - [ ] Create model comparison guide

---

## API Reference

### Mistral API Endpoint

```
POST https://api.mistral.ai/v1/chat/completions
Authorization: Bearer $MISTRAL_API_KEY
```

### Google Gemini API Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
Authorization: Bearer $GOOGLE_API_KEY
```

### Model IDs

| Display Name | Provider | API Model ID |
|:---|:---|:---|
| Mistral Small 3 | Mistral | `mistral-small-latest` |
| Mistral Medium | Mistral | `mistral-medium-latest` |
| Mistral Large | Mistral | `mistral-large-latest` |
| Gemini 2.0 Flash | Google | `gemini-2.0-flash` |
| Gemini 2.0 Pro | Google | `gemini-2.0-pro` |
| Gemini 3.0 Flash | Google | `gemini-3.0-flash` |
| Gemini 3.0 Pro | Google | `gemini-3.0-pro` |

---

## Quality Benchmarks (To Be Completed)

After implementation, run quality tests on the turbojet engine paper:

| Model | BLEU Score | Time (50 pages) | Cost (50 pages) |
|:---|:---|:---|:---|
| gpt-4o-mini | TBD | TBD | TBD |
| gpt-4o | TBD | TBD | TBD |
| mistral-small-3 | TBD | TBD | TBD |
| mistral-medium | TBD | TBD | TBD |
| mistral-large | TBD | TBD | TBD |
| gemini-2.0-flash | TBD | TBD | TBD |
| gemini-2.0-pro | TBD | TBD | TBD |
| gemini-3.0-flash | TBD | TBD | TBD |
| gemini-3.0-pro | TBD | TBD | TBD |

---

## Related Documentation

- [Worker Orchestration](../../worker-orchestration.md) – Current model recommendations
- [Version 0.1.1](../version%200.1.1/version%200.1.1.md) – Bug fixes (prerequisite)
