from app import create_app

# Create the application instance using the default config
app = create_app('development')

if __name__ == '__main__':
    # Run the server
    # host='0.0.0.0' makes it accessible on your local network
    app.run(debug=True, host='0.0.0.0', port=5000)