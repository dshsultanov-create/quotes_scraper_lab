from scraper import sheets_sync


def test_send_rows(monkeypatch):
    sent_requests = []

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "success": True,
                "type": "quotes",
                "rows_received": 1,
            }

    def fake_post(url, json, timeout):
        sent_requests.append(
            {
                "url": url,
                "json": json,
                "timeout": timeout,
            }
        )

        return FakeResponse()

    monkeypatch.setattr(
        sheets_sync,
        "WEB_APP_URL",
        "https://example.com/fake-web-app",
    )

    monkeypatch.setattr(
        sheets_sync,
        "API_TOKEN",
        "fake-test-token",
    )

    monkeypatch.setattr(
        sheets_sync.requests,
        "post",
        fake_post,
    )

    rows = [
        {
            "id": 1,
            "quote_text": "Test quote",
        }
    ]

    result = sheets_sync.send_rows(
        "quotes",
        rows,
    )

    assert result == {
        "success": True,
        "type": "quotes",
        "rows_received": 1,
    }

    assert len(sent_requests) == 1

    request = sent_requests[0]

    assert (
        request["url"]
        == "https://example.com/fake-web-app"
    )

    assert request["timeout"] == 30

    assert request["json"] == {
        "token": "fake-test-token",
        "type": "quotes",
        "rows": rows,
    }


def test_send_rows_rejects_api_error(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "success": False,
                "error": "Invalid token.",
            }

    def fake_post(url, json, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        sheets_sync,
        "WEB_APP_URL",
        "https://example.com/fake-web-app",
    )

    monkeypatch.setattr(
        sheets_sync,
        "API_TOKEN",
        "fake-test-token",
    )

    monkeypatch.setattr(
        sheets_sync.requests,
        "post",
        fake_post,
    )

    try:
        sheets_sync.send_rows(
            "quotes",
            [],
        )

        assert False, "RuntimeError was not raised"

    except RuntimeError as error:
        assert str(error) == "Invalid token."