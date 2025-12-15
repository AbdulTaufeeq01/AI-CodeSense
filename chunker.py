def chunk_code(code, chunk_size=30):
    lines = code.split("\n")
    return [
        "\n".join(lines[i:i + chunk_size])
        for i in range(0, len(lines), chunk_size)
    ]
