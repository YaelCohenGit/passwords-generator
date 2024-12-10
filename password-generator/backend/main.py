import secrets
import string
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")



@app.get("/generate-password/")
async def generate_password(
        length: int = Query(12, le=128, description="Password length (1-128)"),  # Removed ge=6
        include_uppercase: bool = Query(True, description="Include uppercase letters"),
        include_lowercase: bool = Query(True, description="Include lowercase letters"),
        include_digits: bool = Query(True, description="Include digits"),
        include_special: bool = Query(True, description="Include special characters"),
        include_word: str = Query(None, description="A specific word to include in the password")
):
    """
    API endpoint to generate a strong password based on query parameters.

    :param length: The desired length of the password (default: 12, range: 6-128).
    :param include_uppercase: Whether to include uppercase letters.
    :param include_lowercase: Whether to include lowercase letters.
    :param include_digits: Whether to include digits.
    :param include_special: Whether to include special characters.
    :param include_word: A specific word to include in the password.
    :return: A JSON response with the generated password.
    """
    # Build the character pool based on query parameters
    alphabet = ""
    if include_uppercase:
        alphabet += string.ascii_uppercase
    if include_lowercase:
        alphabet += string.ascii_lowercase
    if include_digits:
        alphabet += string.digits
    if include_special:
        alphabet += string.punctuation

    # Ensure at least one type of character is included
    if not alphabet:
        raise HTTPException(
            status_code=400,
            detail="At least one type of character must be selected."
        )

    # Adjust length if a specific word is provided
    if include_word:
        if len(include_word) >= length:
            raise HTTPException(
                status_code=400,
                detail="The specific word must be shorter than the password length."
            )
        length -= len(include_word)

    # Generate the random part of the password
    random_part = ''.join(secrets.choice(alphabet) for _ in range(length))

    # Combine the word and random part randomly
    if include_word:
        password_list = list(random_part)
        insert_position = secrets.randbelow(len(password_list) + 1)
        password_list.insert(insert_position, include_word)
        password = ''.join(password_list)
    else:
        password = random_part

    return {"password": password}
#examples of requests:
#GET /generate-password/?length=10&include_special=false
#GET /generate-password/?length=8&include_uppercase=false&include_lowercase=false&include_special=false
# GET /generate-password/?length=16&include_uppercase=true&include_digits=true&include_word=MyWord


def is_password_strong(password: str) -> str:
    score = 0

    # אורך הסיסמה
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    # מאפייני תווים
    if any(char.isdigit() for char in password):  # מכיל ספרות
        score += 1
    if any(char.islower() for char in password):  # מכיל אותיות קטנות
        score += 1
    if any(char.isupper() for char in password):  # מכיל אותיות גדולות
        score += 1
    if any(char in string.punctuation for char in password):  # מכיל תווים מיוחדים
        score += 1

    # החזרת החוזק על בסיס ציון
    if score < 3:
        return "Weak"
    elif score == 3:
        return "Fair"
    elif score == 4:
        return "Strong"
    elif score >= 5:
        return "Very Strong"

    return "Weak"  # ברירת מחדל



@app.get("/check-password-strength/")
async def check_password_strength(password: str = Query(..., min_length=1)):
    strength = is_password_strong(password)
    tips = []
    if len(password) < 6:
        tips.append("Consider using a password with at least 6 characters.")
    if not any(char.isdigit() for char in password):
        tips.append("Include at least one digit.")
    if not any(char.isupper() for char in password):
        tips.append("Include at least one uppercase letter.")
    if not any(char in string.punctuation for char in password):
        tips.append("Include at least one special character.")
    return {"password": password, "strength": strength, "tips": tips}
#examples of requests:
#GET http://127.0.0.1:8000/check-password-strength/?password=MyStrongP@ssw0rd
#GET /check-password-strength/?password=12345






if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


