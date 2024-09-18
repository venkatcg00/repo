import hashlib

def generate_md5(row):
    # Concatenate the row values into a single string
    row_string = ''.join(row.astype(str))

    # Generate MD5 hash
    return hashlib.md5(row_string.encode()).hexdigest()