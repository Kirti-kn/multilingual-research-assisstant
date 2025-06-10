from supabase import create_client
import os

SUPABASE_URL = "https://vhyjzvksnrrwpuqaioyk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoeWp6dmtzbnJyd3B1cWFpb3lrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk1OTAwMDYsImV4cCI6MjA2NTE2NjAwNn0.4v7S8LO1x4UMN67AnhMmsfzoPBSRBn-za6F_8Q-Iz90"
BUCKET_NAME = "pdfs"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(filepath):
    filename = os.path.basename(filename)
    with open(filepath, "rb") as f:
        res = supabase.storage.from_(BUCKET_NAME).upload(filename, f, {"cache-control":"3600", "upsert": True})
    if res.get("error"):
        raise Exception(f"Upload failed: {res['error']['message']}")
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}" 