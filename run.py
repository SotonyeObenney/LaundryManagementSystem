from app import create_app

laundry_app = create_app()

if __name__ == "__main__":
    laundry_app.run(debug=True)