import typer
import bcrypt
from db.models.user import User
from db.session import SessionLocal

app = typer.Typer(help="Management commands for ContextIQ")
user_app = typer.Typer(help="User related commands")

# Register subcommand group
app.add_typer(user_app, name="user")

@user_app.command("create-admin")
def create_admin():
    """Create an admin user interactively."""
    db = SessionLocal()
    try:
        email = typer.prompt("Enter admin email")
        password = typer.prompt("Enter password", hide_input=True, confirmation_prompt=True)

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            typer.echo("⚠️ Admin with this email already exists.")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(email=email, password=hashed_pw, is_admin=True, is_superuser=True)
        db.add(user)
        db.commit()
        typer.echo("✅ Admin user created successfully.")
    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    app()

if __name__ == "__main__":
    main()
