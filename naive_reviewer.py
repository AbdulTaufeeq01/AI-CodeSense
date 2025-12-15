from reviewer import review_code

def review_full_repo(files):
    full_context = "\n\n".join(files)
    return review_code(full_context), full_context
