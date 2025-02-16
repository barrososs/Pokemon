from flask import Blueprint, redirect, url_for, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from resources.Config import Config
from flask_jwt_extended import create_access_token

# Configuracion Google OAuth

google_bp = make_google_blueprint(
    client_id=Config.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=Config.GOOGLE_OAUTH_CLIENT_SECRET,
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_url="/auth/callback"
)


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/callback")
def callback():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        # Obtener la información del usuario desde Google

        response = google.get("/oauth2/v2/userinfo")
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Error al obtener información de usuario: {e}"}), 400
    user_info = response.json()
    # Generar token JWT usando, por ejemplo, el email del usuario como identidad
    token = create_access_token(identity=user_info.get("email"))
    return jsonify({
        "msg": "Autenticación exitosa",
        "token": token,
        "user": {
            "email": user_info.get("email"),
            "name": user_info.get("name")
        }
    })
