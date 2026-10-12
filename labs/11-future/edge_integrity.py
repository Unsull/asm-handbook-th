"""Lab-only HMAC manifest + SHA-256 + in-memory replay checking."""
import hashlib
import hmac
import json

TEST_KEY = b'lab-only-do-not-use-in-production'


def serialize(manifest):
    return json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()


def signature(manifest):
    return hmac.new(TEST_KEY, serialize(manifest), hashlib.sha256).hexdigest()


def validate(payload: bytes, manifest: dict, submitted_signature: str, seen_ids: set):
    required = {'device_id', 'capture_id', 'sha256'}
    if not isinstance(manifest, dict) or not required <= manifest.keys():
        return 'INVALID_MANIFEST'
    if manifest['device_id'] != 'lab-kiosk-01':
        return 'UNKNOWN_DEVICE'
    if not hmac.compare_digest(signature(manifest), str(submitted_signature)):
        return 'INVALID_AUTH'
    actual_digest = hashlib.sha256(payload).hexdigest()
    if not hmac.compare_digest(actual_digest, str(manifest['sha256'])):
        return 'INTEGRITY_MISMATCH'
    capture_id = str(manifest['capture_id'])
    if capture_id in seen_ids:
        return 'REPLAY'
    seen_ids.add(capture_id)
    return 'ACCEPTED_FOR_FURTHER_VALIDATION'


def sample():
    body = b'example offline kiosk order (synthetic)'
    manifest = {'device_id': 'lab-kiosk-01', 'capture_id': 'capture-001', 'sha256': hashlib.sha256(body).hexdigest()}
    auth = signature(manifest)
    seen = set()
    return [validate(body+b'!', manifest, auth, seen), validate(body, manifest, auth, seen), validate(body, manifest, auth, seen)]


if __name__ == '__main__':
    print(*sample(), sep='\n')
