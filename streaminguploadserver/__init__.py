import http, multipart, os, pathlib, uploadserver

DISK_LIMIT = 2 ** 40

# Receive streaming uploads
def receive_streaming_upload(handler):
    assert hasattr(uploadserver.args, 'allow_replace')
    assert (
        hasattr(uploadserver.args, 'directory')
        and type(uploadserver.args.directory) is str
    )

    # Initialize multipart parser
    boundary = None
    (content_type, content_type_options) = multipart.parse_options_header(handler.headers['Content-Type'])
    if content_type_options and 'boundary' in content_type_options:
        boundary = content_type_options['boundary']
    content_length = int(handler.headers['Content-Length'])
    multipart_parser = multipart.MultipartParser(handler.rfile, boundary, content_length=content_length, disk_limit=DISK_LIMIT)

    # Persist uploaded files to disk
    files_uploaded = 0
    destination_directory_path = pathlib.Path(uploadserver.args.directory)
    for multipart_part in multipart_parser.get_all('files'):
        if multipart_part.file and multipart_part.filename:
            destination_path = destination_directory_path / pathlib.Path(multipart_part.filename).resolve().name
            if os.path.exists(destination_path) and not (uploadserver.args.allow_replace and os.path.isfile(destination_path)):
                destination_path = uploadserver.auto_rename(destination_path)
            multipart_part.save_as(destination_path)
            multipart_part.close()
            files_uploaded += 1
            handler.log_message(f'Uploaded "{destination_path}"')

    if files_uploaded < 1:
        return (http.HTTPStatus.BAD_REQUEST, 'No files selected')

    # Upload successful
    handler.log_message(f'Finished uploading {files_uploaded} file(s)')
    return (http.HTTPStatus.NO_CONTENT, None)


uploadserver.receive_upload = receive_streaming_upload


def main():
    uploadserver.main()
