def show_api_error(res):
    """
    Convert FastAPI errors into user-friendly messages
    """

    if res is None:
        return "❌ Server is not responding"

    if res.status_code == 404:
        return "❌ Account not found"

    if res.status_code == 400:
        return "❌ Invalid request"

    if res.status_code == 422:
        return "❌ Invalid input data"

    if res.status_code == 409:
        return "❌ Conflict occurred"

    if res.status_code >= 500:
        return "❌ Server error. Please try again later"

    # fallback (safe)
    try:
        return res.json().get("detail", "❌ Something went wrong")
    except Exception:
        return "❌ Something went wrong"
