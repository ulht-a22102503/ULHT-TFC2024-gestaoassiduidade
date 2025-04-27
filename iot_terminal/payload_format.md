# Websockets for terminal UI

## This file specifies the format of the payload for each function

### Fingerprint auth

**Expected format:**

```json
 {
        "auth": string,
        "type": string,
        "id": int,
        "name": string,
        "issues": int,
    }
```

**Expected values:**

- **auth**: `success` or `failure`
- **type**: `fingerprint` or `PIN`
- **id**: employee number
- **name**: employee name
- **issues**: number of anomalies

### PIN auth

1. Client to server
   **Expected format:**

```json
 {
        "type": string,
        "id": int,
        "credential": int,
    }
```

**Expected values:**

- **type**: `fingerprint` or `PIN`
- **id**: employee number
- **credential**: the actual pincode

2. Server reply
   **Expected format:**

```json
 {
        "auth": string,
        "type": string,
        "id": int,
        "name": string,
        "issues": int,
    }
```

**Expected values:**

- **auth**: `success` or `failure`
- **type**: `fingerprint` or `PIN`
- **id**: employee number
- **name**: employee name
- **issues**: number of anomalies

### Enroll fingerprint

**Expected format:**

```json
{
    "type" : string,
    "id" : int,
}
```

**Expected values:**

- **type**: `enroll`
- **id**: employee number
