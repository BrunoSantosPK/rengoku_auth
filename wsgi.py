from auth.app import application


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=3636, debug=True)
