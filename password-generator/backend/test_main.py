from fastapi.testclient import TestClient
from main import app  # ייבוא האפליקציה שלך

client = TestClient(app)

def test_generate_password():
    # בדיקה בסיסית של מחולל הסיסמאות
    response = client.get("/generate-password/", params={
        "length": 12,
        "include_uppercase": True,
        "include_lowercase": True,
        "include_digits": True,
        "include_special": True
    })
    assert response.status_code == 200
    data = response.json()
    assert "password" in data
    assert len(data["password"]) == 12

def test_generate_password_with_word():
    # בדיקה למקרה של הכללת מילה
    response = client.get("/generate-password/", params={
        "length": 16,
        "include_uppercase": True,
        "include_digits": True,
        "include_word": "MyWord"
    })
    assert response.status_code == 200
    data = response.json()
    assert "password" in data
    assert len(data["password"]) == 16
    assert "MyWord" in data["password"]

def test_generate_password_invalid_length():
    # בדיקה למקרה של אורך לא תקין
    response = client.get("/generate-password/", params={
        "length": 4,  # אורך קצר מדי
        "include_uppercase": True,
        "include_lowercase": True,
    })
    assert response.status_code == 422  # FastAPI מחזירה שגיאה עבור ערכים לא תקינים

def test_check_password_strength():
    # בדיקה של חיזוק סיסמאות
    response = client.get("/check-password-strength/", params={
        "password": "MyStrongP@ssw0rd"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["strength"] == "Very Strong"
    assert "tips" in data
