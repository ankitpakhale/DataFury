from bottle import Bottle, request, response, static_file, run
import boto3
import os

app = Bottle()
s3 = boto3.client("s3", region_name="ap-south-1")  # Specify the region here

TEMP_DIR = "temp_downloads"  # Directory to save downloaded files
os.makedirs(TEMP_DIR, exist_ok=True)  # Create temp directory if it doesn't exist


# Function to handle CORS
def set_cors_headers():
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"


@app.route("/list-files", method=["OPTIONS", "POST"])
def list_files():
    set_cors_headers()

    if request.method == "OPTIONS":
        return {}  # Preflight request, just return 200

    data = request.json
    bucket_name = data.get("bucket_name")

    if not bucket_name:
        return {"error": "Bucket name is required"}, 400

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            files = [
                obj["Key"] for obj in response["Contents"][:4]
            ]  # Get only the first 4 files
            return {"files": files}
        else:
            return {"error": "No files found in the bucket."}, 404

    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/download-file")
def download_file():
    set_cors_headers()

    file_key = request.query.file_path
    bucket_name = request.query.bucket_name  # Include bucket name for download

    if not bucket_name or not file_key:
        return {"error": "File path and bucket name are required"}, 400

    local_file_path = os.path.join(TEMP_DIR, file_key)

    try:
        # Download file from S3 to local path if it doesn't exist
        if not os.path.exists(local_file_path):
            s3.download_file(bucket_name, file_key, local_file_path)

        return static_file(local_file_path, root=".", download=True)

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True)
